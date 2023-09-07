#!/usr/bin/env python3
"""
This script does a basic archive of Discourse content by way of its API.

TODO: figure out how to handle post updates.

"""
import urllib.request
import sys
import time
import os
import json
import datetime
from dataclasses import dataclass
from pathlib import Path

import logging

loglevel = 'DEBUG' if os.environ.get('DEBUG') else 'INFO'
try:
    # If `rich` is installed, use pretty logging.
    from rich.logging import RichHandler
    logging.basicConfig(level=loglevel, datefmt="[%X]", handlers=[RichHandler()])
except ImportError:
    logging.basicConfig(level=loglevel)

log = logging.getLogger('archive')


DISCOURSE_URL = os.environ.get('DISCOURSE_URL', 'https://delvingbitcoin.org')
TARGET_DIR = Path(os.environ.get('TARGET_DIR', './archive'))

POSTS_DELAY_SECS = 5


def http_get(path) -> str:
    log.debug("HTTP GET %s", path)
    backoff = 3

    while True:
        try:
            with urllib.request.urlopen(f"{DISCOURSE_URL}{path}") as f:
                return f.read().decode()
        except Exception:
            time.sleep(backoff)
            backoff *= 2

            if backoff >= 256:
                log.exception('ratelimit exceeded, or something else wrong?')
                sys.exit(1)


def http_get_json(path) -> dict:
    try:
        return json.loads(http_get(path))
    except json.JSONDecodeError:
        log.warning("unable to decode JSON response from %r", path)
        raise


class PostSlug:
    @classmethod
    def id_from_filename(cls, name: str) -> int:
        return int(name.split('-', 1)[0])


@dataclass(frozen=True)
class PostTopic:
    id: int
    slug: str
    title: str


@dataclass(frozen=True)
class Post:
    id: int
    slug: str
    raw: dict

    def get_created_at(self) -> datetime.datetime:
        return datetime.datetime.fromisoformat(self.raw['created_at'])

    def get_year(self) -> int:
        return self.get_created_at().year

    def get_month_name(self) -> str:
        dt = self.get_created_at()
        return f"{dt.strftime('%m')}-{dt.strftime('%B')}"

    def save(self, dir: Path):
        """Write the raw post to disk."""
        idstr = str(self.id).zfill(10)
        filename = f"{idstr}-{self.raw['username']}-{self.raw['topic_slug']}.json"
        rel_path = Path(str(self.get_year())) / self.get_month_name() / filename
        full_path = dir / rel_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        log.info("saving post %s to %s", self.id, full_path)
        full_path.write_text(json.dumps(self.raw, indent=2))

    def get_topic(self) -> PostTopic:
        return PostTopic(
            id=self.raw['topic_id'],
            slug=self.raw['topic_slug'],
            title=self.raw['topic_title'],
        )

    @classmethod
    def from_json(cls, j: dict) -> 'Post':
        return cls(
            id=j['id'],
            slug=j['topic_slug'],
            raw=j,
        )


@dataclass(frozen=True)
class Topic:
    id: int
    slug: str
    raw: dict
    markdown: str

    def get_created_at(self) -> datetime.datetime:
        return datetime.datetime.fromisoformat(self.raw['created_at'])

    def get_year(self) -> int:
        return self.get_created_at().year

    def get_month_name(self) -> str:
        dt = self.get_created_at()
        return f"{dt.strftime('%m')}-{dt.strftime('%B')}"

    def save_rendered(self, dir: Path):
        """Write the rendered (.md) topic to disk."""
        idstr = str(self.id).zfill(10)
        date = str(self.get_created_at().date())
        filename = f"{idstr}-{date}-{self.slug}.md"

        rel_path = Path(str(self.get_year())) / self.get_month_name() / filename
        full_path = dir / rel_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        log.info("saving topic markdown %s to %s", self.id, full_path)
        markdown = f"# {self.raw['title']}\n\n{self.markdown}"
        full_path.write_text(markdown)

    def get_topic(self) -> PostTopic:
        return PostTopic(
            id=self.raw['topic_id'],
            slug=self.raw['topic_slug'],
            title=self.raw['topic_title'],
        )

    @classmethod
    def from_json(cls, t: dict, markdown: str) -> 'Topic':
        return cls(
            id=t['id'],
            slug=t['slug'],
            raw=t,
            markdown=markdown,
        )


def main():
    (posts_dir := TARGET_DIR / 'posts').mkdir(parents=True, exist_ok=True)
    (topics_dir := TARGET_DIR / 'rendered-topics').mkdir(parents=True, exist_ok=True)

    latest_id = None
    for yr_dir in sorted(posts_dir.glob('*'), reverse=True)[:1]:
        for month_dir in sorted(yr_dir.glob('*'), reverse=True)[:1]:
            for post in sorted(month_dir.glob('*.json'), reverse=True)[:1]:
                latest_id = PostSlug.id_from_filename(post.name)

    log.info("detected latest post id as %s", latest_id)

    topics_to_get = {}
    last_id_processed = None

    posts = http_get_json('/posts.json')['latest_posts']

    while posts:
        log.info("processing %d posts", len(posts))
        for json_post in posts:
            try:
                post = Post.from_json(json_post)
            except Exception:
                log.warning("failed to deserialize post %s", json_post)
                raise
            post.save(posts_dir)
            last_id_processed = post.id
            topic = post.get_topic()
            topics_to_get[topic.id] = topic

        if latest_id is not None and last_id_processed < latest_id:
            break
        if last_id_processed <= 1:
            break

        time.sleep(POSTS_DELAY_SECS)
        posts = http_get_json(
            f'/posts.json?before={last_id_processed - 1}')['latest_posts']

        # Discourse implicitly limits the posts query for IDs between `before` and
        # `before - 50`, so if we don't get any results we have to kind of scan.
        while not posts and last_id_processed >= 0:
            # This is probably off-by-one, but doesn't hurt to be safe.
            last_id_processed -= 49
            posts = http_get_json(
                f'/posts.json?before={last_id_processed}')['latest_posts']
            time.sleep(1)

    time.sleep(3)

    for topic in topics_to_get.values():
        data = http_get_json(f"/t/{topic.id}.json")
        body = http_get(f"/raw/{topic.id}")

        if not body:
            log.warning("could not retrieve topic %d markdown", topic.id)
            continue

        t = Topic.from_json(data, body)
        t.save_rendered(topics_dir)
        log.info("saved topic %s (%s)", t.id, t.slug)

        time.sleep(0.3)


if __name__ == "__main__":
    main()
