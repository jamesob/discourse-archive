# archive-discourse

A script that provides a basic archive of Discourse contents.

You'll have to read the script to determine which environment variables
need to be set for your particular Discourse installation.

The structure that it generates looks something like:
```
archive
├── posts
│   ├── 2022
│   │   └── 08-August
│   │       ├── 0000000001-system-about-the-meta-category.json
│   │       ├── 0000000010-system-welcome-to-delving-bitcoin.json
│   │       ├── 0000000016-admin-about-the-philosophy-category.json
│   │       └── 0000000048-RubenSomsen-deflationary-money-is-a-good-thing.json
│   └── 2023
│       ├── 01-January
│       │   ├── 0000000055-ajtowns-lightning-fees-inbound-vs-outbound.json
│       │   ├── 0000000057-renepickhardt-lightning-fees-inbound-vs-outbound.json
│       │   ├── 0000000058-ajtowns-lightning-fees-inbound-vs-outbound.json
│       │   ├── 0000000059-renepickhardt-lightning-fees-inbound-vs-outbound.json
│       │   └── 0000000060-ajtowns-lightning-fees-inbound-vs-outbound.json
│       └── 09-September
│           ├── 0000000167-Ajian-thoughts-on-scaling-and-consensus-changes-2023.json
│           ├── 0000000172-jamesob-public-archive-for-delving-bitcoin.json
│           ├── 0000000173-ajtowns-public-archive-for-delving-bitcoin.json
│           ├── 0000000174-jamesob-public-archive-for-delving-bitcoin.json
│           ├── 0000000175-ajtowns-public-archive-for-delving-bitcoin.json
│           └── 0000000178-midnight-public-archive-for-delving-bitcoin.json
└── rendered-topics
    ├── 2022
    │   └── 08-August
    │       ├── 0000000001-2022-08-24-about-the-meta-category.md
    │       ├── 0000000021-2022-08-24-proof-of-micro-burn-burning-btc-while-minimizing-on-chain-block-space-usage.md
    │       └── 0000000022-2022-08-24-deflationary-money-is-a-good-thing.md
    └── 2023
        ├── 01-January
        │   └── 0000000029-2023-01-10-lightning-fees-inbound-vs-outbound.md
        ├── 08-August
        │   ├── 0000000032-2023-08-16-thoughts-on-scaling-and-consensus-changes-2023.md
        │   ├── 0000000055-2023-08-22-op-vault-fanfiction-for-rate-limited-and-collateralized-unvaulting.md
        │   └── 0000000060-2023-08-23-combined-ctv-apo-into-minimal-txhash-csfs.md
        └── 09-September
            └── 0000000087-2023-09-05-public-archive-for-delving-bitcoin.md
```
