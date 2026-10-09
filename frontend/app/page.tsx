'use client';

import { FormEvent, useState } from 'react';
import { createClient } from 'genlayer-js';
import { studionet } from 'genlayer-js/chains';

const contractAddress = process.env.NEXT_PUBLIC_CONTRACT_ADDRESS as `0x${string}` | undefined;

export default function Home() {
  const [claim, setClaim] = useState('');
  const [sourceA, setSourceA] = useState('');
  const [sourceB, setSourceB] = useState('');
  const [status, setStatus] = useState('');
  const [result, setResult] = useState('');

  async function verify(event: FormEvent) {
    event.preventDefault();

    if (!contractAddress) {
      setStatus('Add NEXT_PUBLIC_CONTRACT_ADDRESS to .env.local first.');
      return;
    }

    if (!window.ethereum) {
      setStatus('Please install MetaMask or another EIP-1193 wallet.');
      return;
    }

    try {
      setStatus('Connecting wallet...');
      const accounts = await window.ethereum.request({
        method: 'eth_requestAccounts',
      }) as string[];

      const client = createClient({
        chain: studionet,
        account: accounts[0] as `0x${string}`,
        provider: window.ethereum,
      });

      await client.connect('studionet');
      setStatus('Submitting verification transaction...');

      const txHash = await client.writeContract({
        address: contractAddress,
        functionName: 'verify_claim',
        args: [claim, sourceA, sourceB],
        value: BigInt(0),
      });

      setStatus(`Transaction submitted: ${txHash}`);

     const receipt = await client.waitForTransactionReceipt({
  hash: txHash,
  waitUntil: 'finalized',
  interval: 5000,
  retries: 100,
});

      setStatus(
        `Finalized. Execution result: ${String(
          receipt.txExecutionResultName ?? 'unknown'
        )}`
      );

      const value = await client.readContract({
        address: contractAddress,
        functionName: 'get_result',
        args: [],
      });

      setResult(String(value));
    } catch (error) {
      setStatus(error instanceof Error ? error.message : String(error));
    }
  }

  return (
    <main className="shell">
      <section className="hero">
        <div className="badge">GENLAYER • CONSENSUS VERIFICATION</div>
        <h1>Truth<span>Resolve</span></h1>
        <p>
          Compare real-world evidence and reach a consensus-backed verdict
          using a GenLayer Intelligent Contract.
        </p>
      </section>

      <form onSubmit={verify} className="card">
        <label>
          Claim
          <textarea
            value={claim}
            onChange={(e) => setClaim(e.target.value)}
            placeholder="Example: Organization X published announcement Y."
            required
          />
        </label>

        <label>
          Source A
          <input
            value={sourceA}
            onChange={(e) => setSourceA(e.target.value)}
            placeholder="https://..."
            type="url"
            required
          />
        </label>

        <label>
          Source B
          <input
            value={sourceB}
            onChange={(e) => setSourceB(e.target.value)}
            placeholder="https://..."
            type="url"
            required
          />
        </label>

        <button type="submit">Verify with GenLayer →</button>
        <p className="status">{status}</p>
      </form>

      {result && (
        <section className="card result">
          <h2>Consensus result</h2>
          <pre>{result}</pre>
        </section>
      )}

      <footer>
        TruthResolve is a prototype for source-grounded verification. It is
        not a substitute for professional or emergency advice.
      </footer>
    </main>
  );
}

declare global {
  interface Window {
    ethereum?: {
      request: (args: {
        method: string;
        params?: unknown[];
      }) => Promise<unknown>;
    };
  }
}
