import React from "react";

function WalletList({ wallets }) {
  return (
    <div>
      <h2>Wallets</h2>
      <ul>
        {wallets.map((wallet) => (
          <li key={wallet.id}>
            {wallet.currency}: {wallet.balance}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default WalletList;