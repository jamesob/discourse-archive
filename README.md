# discourse-archive

A script that provides a basic archive of Discourse contents.


## Usage

```
% pip install discourse-archive

% discourse-archive --help
usage: discourse-archive [-h] [-u URL] [--debug] [-t TARGET_DIR]

Create a basic content archive from a Discourse installation

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     URL of the Discourse server
  --debug
  -t TARGET_DIR, --target-dir TARGET_DIR
                        Target directory for the archive
```

The structure that it generates looks something like:
```
archive
├── posts
│   ├── 2022-08-August
│   │   ├── 0000000001-system-about-the-meta-category.json
│   │   ├── 0000000046-RubenSomsen-deflationary-money-is-a-good-thing.json
│   │   ├── 0000000047-ajtowns-deflationary-money-is-a-good-thing.json
│   │   └── 0000000048-RubenSomsen-deflationary-money-is-a-good-thing.json
│   ├── 2023-08-August
│   │   ├── 0000000062-jamesob-thoughts-on-scaling-and-consensus-changes-2023.json
│   │   ├── 0000000120-instagibbs-op-vault-fanfiction-for-rate-limited-and-collateralized-unvaulting.json
│   │   ├── 0000000121-instagibbs-op-vault-fanfiction-for-rate-limited-and-collateralized-unvaulting.json
│   │   ├── 0000000143-naumenkogs-proof-of-micro-burn-burning-btc-while-minimizing-on-chain-block-space-usage.json
│   │   ├── 0000000144-RubenSomsen-proof-of-micro-burn-burning-btc-while-minimizing-on-chain-block-space-usage.json
│   │   └── 0000000157-instagibbs-op-vault-fanfiction-for-rate-limited-and-collateralized-unvaulting.json
│   └── 2023-09-September
│       ├── 0000000167-Ajian-thoughts-on-scaling-and-consensus-changes-2023.json
│       ├── 0000000172-jamesob-public-archive-for-delving-bitcoin.json
│       ├── 0000000173-ajtowns-public-archive-for-delving-bitcoin.json
│       ├── 0000000174-jamesob-public-archive-for-delving-bitcoin.json
│       ├── 0000000175-ajtowns-public-archive-for-delving-bitcoin.json
│       └── 0000000178-midnight-public-archive-for-delving-bitcoin.json
└── rendered-topics
    ├── 2022-08-August
    │   ├── 2022-08-24-about-the-economics-category-id14.md
    │   ├── 2022-08-24-about-the-implementation-category-id16.md
    │   ├── 2022-08-24-design-for-algorithmic-stablecoin-backed-by-btc-id20.md
    │   ├── 2022-08-24-proof-of-micro-burn-burning-btc-while-minimizing-on-chain-block-space-usage-id21.md
    │   └── 2022-08-24-welcome-to-delving-bitcoin-id7.md
    ├── 2023-01-January
    │   └── 2023-01-10-lightning-fees-inbound-vs-outbound-id29.md
    ├── 2023-08-August
    │   ├── 2023-08-16-thoughts-on-scaling-and-consensus-changes-2023-id32.md
    │   ├── 2023-08-22-op-vault-fanfiction-for-rate-limited-and-collateralized-unvaulting-id55.md
    │   └── 2023-08-23-combined-ctv-apo-into-minimal-txhash-csfs-id60.md
    └── 2023-09-September
        └── 2023-09-05-public-archive-for-delving-bitcoin-id87.md
```
