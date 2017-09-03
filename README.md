# docker-play-speech-api
Docker Yandex speechkit and api for remote play speech

Use: https://github.com/art1415926535/Yandex_speech

1. Get API‑key for Yandex speech kit:
https://developer.tech.yandex.ru/

2. Run app:
```bash
make build
YANDEX_KEY=test PORT=5000 make run
```

3. Example request:
```bash
curl -i -H "Content-Type: application/json" -X POST -d '{"text": "Привет!", "speaker":"omazh", "emotion":"good"}' http://127.0.0.1:5000/play
```
- text - Text to speech: "з+амок" (before the stressed vowel can be put "+"; the restriction on line length: 2000 bytes);
- speaker (optional) - Speaker. Female: "jane" (by default), "oksana", "alyss", "omazh". Male: "zahar", "ermil";
- lang (optional) - Language: "ru‑RU" (by default), "en-US", "tr-TR", "uk-UK";
- emotion (optional) - The color of the voice: "neutral" (by default), "evil", "good";
- speed (optional) - Speech tempo: a value between 0.1 (slowest) to 3.0 (fastest).


4. Shutdown app:
```bash
curl -i http://127.0.0.1:5000/kill
```
