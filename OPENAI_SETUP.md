# 🔑 OpenAI API Setup Guide

## Fixing "Quota Exceeded" Error

The "quota exceeded" error means your OpenAI API account doesn't have available credits or billing isn't set up.

### Step 1: Check Your API Key

1. **Verify your API key is correct:**
   - Check `key.txt` in the project root
   - Make sure it starts with `sk-` and is complete
   - No extra spaces or newlines

2. **Get a new API key:**
   - Go to https://platform.openai.com/api-keys
   - Sign in or create an account
   - Click "Create new secret key"
   - Copy the key (you can only see it once!)
   - Save it to `key.txt` in your project root

### Step 2: Set Up Billing (Required)

OpenAI requires a payment method even for free tier usage:

1. **Go to OpenAI Billing:**
   - Visit https://platform.openai.com/account/billing
   - Sign in to your account

2. **Add Payment Method:**
   - Click "Add payment method"
   - Enter your credit card details
   - Even if you use free credits, billing must be set up

3. **Set Usage Limits (Optional but Recommended):**
   - Go to https://platform.openai.com/account/billing/limits
   - Set a monthly spending limit to avoid surprises
   - Start with $5-10/month for testing

### Step 3: Check Your Usage & Credits

1. **Check Usage Dashboard:**
   - Visit https://platform.openai.com/usage
   - See how much you've used
   - Check remaining credits

2. **Check Account Credits:**
   - Free tier: $5 free credits (if available)
   - Paid tier: Pay-as-you-go

### Step 4: Verify API Key in Code

Your API key should be in `key.txt`:

```
sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Or set as environment variable:
```bash
# Windows PowerShell
$env:OPENAI_API_KEY="sk-proj-..."

# Windows CMD
set OPENAI_API_KEY=sk-proj-...

# Linux/Mac
export OPENAI_API_KEY="sk-proj-..."
```

### Step 5: Test Your API Key

Test if your key works:

```python
from openai import OpenAI

client = OpenAI(api_key="your-key-here")
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello"}]
)
print(response.choices[0].message.content)
```

## Common Issues & Solutions

### Issue: "Insufficient quota"
**Solution:**
- Add payment method to your OpenAI account
- Add credits to your account
- Check if you've exceeded free tier limits

### Issue: "Invalid API key"
**Solution:**
- Verify the key in `key.txt` is correct
- Make sure there are no extra spaces
- Regenerate the key if needed

### Issue: "Rate limit exceeded"
**Solution:**
- You're making too many requests too fast
- Wait a few minutes and try again
- Consider upgrading your tier

### Issue: "Model not found"
**Solution:**
- The model `gpt-4o-mini` might not be available in your region
- Try `gpt-3.5-turbo` instead (cheaper too)
- Update `api/llm_agent.py` line 224 to use a different model

## Cost Estimates

**gpt-4o-mini** (current model):
- Input: $0.15 per 1M tokens
- Output: $0.60 per 1M tokens
- ~$0.001-0.01 per typical StockBot query

**gpt-3.5-turbo** (cheaper alternative):
- Input: $0.50 per 1M tokens  
- Output: $1.50 per 1M tokens
- ~$0.0005-0.005 per typical StockBot query

## Alternative: Use Cheaper Model

If you want to reduce costs, edit `api/llm_agent.py`:

```python
# Line 224 - Change from:
model="gpt-4o-mini",

# To:
model="gpt-3.5-turbo",  # Cheaper option
```

## Quick Checklist

- [ ] API key is in `key.txt` or environment variable
- [ ] Payment method added to OpenAI account
- [ ] Account has credits/quota available
- [ ] API key is valid and active
- [ ] Tested API key with simple request

## Still Having Issues?

1. **Check OpenAI Status:** https://status.openai.com
2. **Check Account Dashboard:** https://platform.openai.com/account
3. **Contact OpenAI Support:** https://help.openai.com

## Free Alternatives (If OpenAI Doesn't Work)

If you can't use OpenAI, the system will still work with:
- ✅ Real-time stock prices
- ✅ Risk metrics
- ✅ ML/technical analysis
- ✅ News headlines
- ❌ AI-powered conversational responses (requires LLM)

For free LLM options, you could integrate:
- **Ollama** (local LLM - free)
- **Hugging Face** (some free models)
- **Anthropic Claude** (has free tier)
