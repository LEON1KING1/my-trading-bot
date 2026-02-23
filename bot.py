import ccxt
import time
import requests

# --- إعداداتك الخاصة ---
TELEGRAM_TOKEN = '8796658711:AAHu5T95itKX4-XK969bT_pSyujdC3cHexo'
CHAT_ID = '5226069328'

def send_telegram_msg(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': message}
    try:
        # قمنا بإضافة مهلة زمنية (timeout) لضمان عدم توقف الكود إذا كان الإنترنت بطيئاً
        response = requests.post(url, json=payload, timeout=15)
        return response.status_code == 200
    except Exception as e:
        print(f"خطأ في إرسال تلجرام: {e}")
        return False

def main():
    print("جاري محاولة تشغيل البوت...")
    # محاولة إرسال رسالة ترحيب فور التشغيل
    if send_telegram_msg("🚀 يا هلا يا LEON! البوت يعمل الآن من السحاب ويراقب الأسعار."):
        print("تم إرسال رسالة الترحيب بنجاح!")
    else:
        print("فشل إرسال الرسالة، تأكد من أنك بدأت المحادثة مع البوت في تلجرام أولاً.")

    # إعداد منصة باينانس (للقراءة فقط حالياً)
    exchange = ccxt.binance()
    symbol = 'BTC/USDT'

    while True:
        try:
            ticker = exchange.fetch_ticker(symbol)
            last_price = ticker['last']
            
            # إرسال السعر الحالي كل ساعة
            send_telegram_msg(f"📊 سعر {symbol} الحالي: ${last_price}")
            
            # الانتظار لمدة ساعة (3600 ثانية)
            time.sleep(3600) 
        except Exception as e:
            print(f"حدث خطأ في جلب السعر: {e}")
            time.sleep(60) # انتظر دقيقة وأعد المحاولة عند حدوث خطأ

if __name__ == "__main__":
    main()
