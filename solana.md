# For Solana

Solana is settlement after FHE. The chain never runs the matcher and never sees a bid. It records SOL movement and a frozen-supply token. Signing stays on this laptop. Default RPC is devnet; the transactions are real (`?cluster=devnet` on every explorer link).

FHE decides the price on Vultr. Solana is what you can open in an explorer afterward.

## Encrypted purchase / auction receipt NFTs

This is the purchase object. Code: `umbra/solana_wallet.py` (`mint_encrypted_receipt`, `issue_auction_receipts`). Live mints are on disk under `umbra/fixtures/receipts/` with explorer signatures.

One versioned transaction, five instructions:

1. Create a mint account (rent-exempt, Token program).
2. `InitializeMint2` — decimals **0**.
3. Create the recipient’s associated token account.
4. `MintTo` **exactly one**.
5. `SetAuthority` mint authority → **none**.

Supply is permanently 1. That token is the receipt NFT. Winners and losers both get one. At most one `won=True` per lot.

The purchase outcome is **not on-chain**. Win/lose, lot id, and message are AES-GCM (nonce + ciphertext, AAD `umbra-receipt`). The key is `SHA-256("umbra-receipt-v1" ‖ recipient_sk[0:32] ‖ mint)`. Disk stores ciphertext only — never the plaintext outcome. Decrypt requires the recipient keypair (or a one-shot caller-held key if you only had an address).

On-chain proof: you received a 1/1. Off-chain, only the holder can read whether they bought or lost. The desk lists a hashed tag + explorer URL. Raw mint, `auction_id`, and ciphertext are treated as leaks (`umbra/privacy.py`).

## Hops and escrow

After a pass, `umbra/hops.py` builds a one-use path: faucet → ingress → cutout → bid. Fresh keypairs, **no memo program**, keys deleted after the hop. Fail or abort wipes the key directory (`umbra/decide.py`). Spend keys never go to Vultr.

Escrow is custodial: a dedicated local keypair holds SOL until release or refund. Not a program. Lose the key file and the funds stay in that address.

The desk HTTP view is a cutout: hashed nyms, explorer links, no roster, no spend keys, no memo.
