✅ How to Install on Raspberry Pi:
Download the correct binary for your Pi model and OS:

bash
Copy
Edit
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_arm64.tar.gz
Extract it:

bash
Copy
Edit
tar -xvzf piper_arm64.tar.gz
cd piper
Download a voice model:

bash
Copy
Edit
mkdir voices && cd voices
wget https://github.com/rhasspy/piper-voices/releases/download/en_US-lessac-medium/en_US-lessac-medium.onnx
wget https://github.com/rhasspy/piper-voices/releases/download/en_US-lessac-medium/en_US-lessac-medium.onnx.json
Test Piper:

bash
Copy
Edit
./piper --model voices/en_US-lessac-medium.onnx --config voices/en_US-lessac-medium.onnx.json --text "Hello from Raspberry Pi"
