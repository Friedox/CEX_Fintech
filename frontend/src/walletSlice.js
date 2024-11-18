import { createSlice } from '@reduxjs/toolkit';

const walletSlice = createSlice({
    name: 'wallet',
    initialState: {
        balances: {},
    },
    reducers: {
        setBalance(state, action) {
            const { currency, amount } = action.payload;
            state.balances[currency] = amount;
        },
        updateBalance(state, action) {
            const { currency, change } = action.payload;
            if (state.balances[currency] !== undefined) {
                state.balances[currency] += change;
            }
        }
    },
});

export const { setBalance, updateBalance } = walletSlice.actions;
export default walletSlice.reducer;