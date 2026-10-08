# TruthResolve

TruthResolve is a GenLayer-powered verification dApp that checks a real-world claim against two independent web sources and asks a GenLayer Intelligent Contract to reach a consensus-backed verdict.

## What it demonstrates

- GenLayer Intelligent Contract written in Python
- Native web access from a non-deterministic block
- LLM-assisted evidence comparison
- Comparative Equivalence Principle for validator consensus
- Next.js frontend using GenLayerJS
- Wallet connection and contract interaction
- Persistent verification result stored in contract state

## Important

This repository is a complete starting project, but it is **not yet deployed**. Before submitting it to the GenLayer Portal, you must:

1. Deploy `contracts/truth_resolve.py`.
2. Put the resulting contract address in `frontend/.env.local`.
3. Run and test the frontend.
4. Push this repository to your own public GitHub repository.
5. Publish the frontend and put its public URL in the Portal.
6. Add the deployed contract explorer URL and a real demo video/post.

Do not submit placeholder URLs.

## Project structure

```text
TruthResolve/
├── contracts/
│   └── truth_resolve.py
├── tests/
│   └── direct/
│       └── test_truth_resolve.py
├── frontend/
│   ├── app/
│   │   ├── globals.css
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── lib/
│   │   └── genlayer.ts
│   ├── package.json
│   ├── tsconfig.json
│   ├── next-env.d.ts
│   └── .env.example
├── requirements.txt
└── .gitignore
```

## Workflow

1. User enters a claim.
2. User supplies two source URLs.
3. The Intelligent Contract fetches both sources.
4. An LLM extracts evidence and decides whether the claim is supported, contradicted, or unresolved.
5. GenLayer's comparative Equivalence Principle asks validators to check agreement on the important conclusion.
6. The accepted result is stored in contract state.
7. The frontend reads and displays the result.

## Development

### Contract

Python 3.12+ is recommended.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Run direct tests:

```bash
pytest tests/direct/ -v
```

Lint:

```bash
genvm-lint check contracts/truth_resolve.py
```

### Frontend

```bash
cd frontend
npm install
copy .env.example .env.local
npm run dev
```

Open http://localhost:3000.

Set:

```text
NEXT_PUBLIC_CONTRACT_ADDRESS=0xYOUR_DEPLOYED_CONTRACT
NEXT_PUBLIC_NETWORK=studionet
```

## Deployment

The easiest first deployment is hosted GenLayer Studio.

1. Open GenLayer Studio.
2. Create an Intelligent Contract.
3. Paste `contracts/truth_resolve.py`.
4. Deploy it.
5. Copy the contract address.
6. Test `verify_claim`.
7. Put the address into `.env.local`.
8. Test the frontend.
9. Publish the frontend.
10. Add the real GitHub, website, demo and contract links to the Portal.

Use stable authoritative sources for demos. Do not submit placeholder URLs.

## Scope

TruthResolve is a verification prototype, not a legal, medical, financial, or emergency decision system. Consensus means validators agreed on the defined task and evidence; it does not make an external claim universally true.

## License

MIT
