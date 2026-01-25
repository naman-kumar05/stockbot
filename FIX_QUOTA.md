# 🔧 Quick Fix: OpenAI Quota Exceeded

## The Problem
Your API key exists, but your OpenAI account has no available quota/credits.

## Quick Solution (5 minutes)

### Step 1: Go to OpenAI Billing
1. Visit: https://platform.openai.com/account/billing
2. Sign in with your OpenAI account

### Step 2: Add Payment Method
1. Click **"Add payment method"**
2. Enter your credit card details
3. **Important:** Even if you use free credits, billing must be set up

### Step 3: Add Credits (Optional)
1. Click **"Add credits"** or **"Add funds"**
2. Add at least $5-10 to start
3. This gives you immediate quota

### Step 4: Verify Your API Key
1. Go to: https://platform.openai.com/api-keys
2. Make sure your key is active
3. If needed, create a new key and update `key.txt`

## Alternative: Use Cheaper Model

If you want to reduce costs, I can update the code to use `gpt-3.5-turbo` instead of `gpt-4o-mini` (about 3x cheaper).

## Check Your Current Status

Visit these pages to diagnose:
- **Usage:** https://platform.openai.com/usage
- **Billing:** https://platform.openai.com/account/billing
- **API Keys:** https://platform.openai.com/api-keys

## Cost Information

**Current model (gpt-4o-mini):**
- ~$0.001-0.01 per StockBot query
- $5 credit = ~500-5000 queries

**Cheaper option (gpt-3.5-turbo):**
- ~$0.0005-0.005 per query
- $5 credit = ~1000-10000 queries

## Still Not Working?

1. **Check if key is valid:**
   ```python
   from openai import OpenAI
   client = OpenAI(api_key="your-key-from-key.txt")
   response = client.chat.completions.create(
       model="gpt-4o-mini",
       messages=[{"role": "user", "content": "test"}]
   )
   print("✅ Key works!" if response else "❌ Key invalid")
   ```

2. **Check account status:**
   - Go to https://platform.openai.com/account
   - Verify account is active
   - Check for any restrictions

3. **Contact OpenAI Support:**
   - https://help.openai.com
   - They can help with quota/billing issues
