# TradingView → Telegram Signal Bot

TradingView theke Buy/Sell alert asle automatically Telegram e message pathabe.

---

## ধাপ ১: Telegram Bot বানাও

1. Telegram এ `@BotFather` কে খুঁজে বের করো
2. `/newbot` লিখে পাঠাও
3. একটা নাম দাও (যেমন: My Signal Bot)
4. একটা username দাও (অবশ্যই `bot` দিয়ে শেষ হতে হবে, যেমন: `my_signal_alert_bot`)
5. BotFather তোমাকে একটা **Token** দেবে — এটা কপি করে রাখো
   ```
   123456789:ABCdefGHIjklMNOpqrstUVwxyz
   ```

## ধাপ ২: Chat ID বের করো

1. এখন তোমার নতুন বটকে Telegram এ সার্চ করে ওপেন করো, `/start` চাপো বা যেকোনো একটা মেসেজ পাঠাও
2. ব্রাউজারে এই লিংকে যাও (TOKEN এর জায়গায় তোমার Token বসাও):
   ```
   https://api.telegram.org/bot<TOKEN>/getUpdates
   ```
3. সেখানে JSON response এ `"chat":{"id": 123456789, ...}` — এই নাম্বারটাই তোমার Chat ID

> **Group এ পাঠাতে চাইলে:** বটকে group এ add করো, group এ একটা মেসেজ পাঠাও, তারপর একই getUpdates লিংকে group এর id পাবে (এটা সাধারণত negative number হয়, যেমন `-1001234567890`)

## ধাপ ৩: কোড ডাউনলোড ও Deploy করো (Railway ব্যবহার করে, সবচেয়ে সহজ ও ফ্রি)

1. [railway.app](https://railway.app) এ গিয়ে GitHub দিয়ে সাইন আপ করো
2. এই ৩টা ফাইল (`app.py`, `requirements.txt`, `Procfile`) একটা নতুন GitHub repository তে আপলোড করো
3. Railway তে **"New Project" → "Deploy from GitHub repo"** সিলেক্ট করো, তোমার repo বেছে নাও
4. Railway এ **Variables** ট্যাবে গিয়ে এই environment variables গুলো অ্যাড করো:
   ```
   BOT_TOKEN = তোমার Telegram bot token
   CHAT_ID = তোমার chat id
   WEBHOOK_SECRET = (ইচ্ছামত একটা গোপন শব্দ, যেমন: mysecret123)
   ```
5. Deploy হয়ে গেলে Railway একটা URL দেবে, যেমন:
   ```
   https://your-app-name.up.railway.app
   ```

## ধাপ ৪: টেস্ট করো

ব্রাউজারে গিয়ে এই লিংক ওপেন করো:
```
https://your-app-name.up.railway.app/test
```
যদি সব ঠিক থাকে, তোমার Telegram এ একটা টেস্ট মেসেজ চলে আসবে ✅

## ধাপ ৫: TradingView এ Alert সেট করো

1. TradingView এ তোমার chart/strategy ওপেন করো
2. **Alert** বাটনে ক্লিক করো (⏰ আইকন)
3. Condition সেট করো (তোমার strategy/indicator অনুযায়ী)
4. **Notifications** ট্যাবে গিয়ে **Webhook URL** এ এটা বসাও:
   ```
   https://your-app-name.up.railway.app/webhook?secret=mysecret123
   ```
5. **Message** বক্সে এই ফরম্যাটে JSON লিখো:
   ```json
   {
     "ticker": "{{ticker}}",
     "signal": "BUY",
     "price": "{{close}}",
     "time": "{{time}}",
     "timeframe": "{{interval}}"
   }
   ```
   (Sell alert এর জন্য আলাদা alert বানিয়ে `"signal": "SELL"` দিও)
6. **Create** চাপো — ব্যাস, এখন থেকে যখনই এই condition true হবে, তোমার Telegram এ signal চলে আসবে!

---

## Local এ টেস্ট করতে চাইলে

```bash
pip install -r requirements.txt
set BOT_TOKEN=your_token_here
set CHAT_ID=your_chat_id_here
python app.py
```

তারপর `http://localhost:5000/test` এ গিয়ে চেক করো।

---

## গুরুত্বপূর্ণ কথা

- এই বট শুধু **notification/alarm** পাঠায় — এটা কোনো ট্রেড অটো execute করে না, তাই তোমার ফান্ড নিরাপদ থাকে টুলটার কারণে কোনো ঝুঁকি ছাড়াই
- Signal এর accuracy সম্পূর্ণভাবে তোমার TradingView strategy/indicator এর উপর নির্ভর করে — বট শুধু messenger হিসেবে কাজ করে
- `WEBHOOK_SECRET` ব্যবহার করা ভালো, নাহলে যে কেউ তোমার webhook URL পেলে fake signal পাঠাতে পারবে
