# 🤖 AI Bedrock Chatbot

**Production-ready AI chatbot powered by AWS Bedrock Claude 3**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-brightgreen)](https://higuseonhye.github.io/ai-bedrock-chatbot/)
[![AWS](https://img.shields.io/badge/AWS-Bedrock%20Claude%203-orange)](https://aws.amazon.com/bedrock/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## 🌟 Features

- 🚀 **Production-ready** - Deployed on AWS with API Gateway
- 🧠 **Latest AI Model** - Powered by AWS Bedrock Claude 3 Sonnet
- 🌐 **Global Access** - Hosted on GitHub Pages with HTTPS
- 📱 **Responsive Design** - Works perfectly on mobile and desktop
- ⚡ **Real-time Chat** - Instant AI responses with loading indicators
- 🔒 **Secure** - CORS-enabled API with proper authentication
- 💰 **Cost-effective** - Serverless architecture with pay-per-use

## 🎯 Live Demo

**Try it now:** [https://higuseonhye.github.io/ai-bedrock-chatbot/](https://higuseonhye.github.io/ai-bedrock-chatbot/)

## 🏗️ Architecture

```
User Browser (HTTPS)
    ↓
GitHub Pages (Global CDN)
    ↓
AWS API Gateway (CORS + Auth)
    ↓
AWS Lambda (Python 3.13)
    ↓
AWS Bedrock Claude 3 Sonnet
```

## ⚡ Quick Start

### Prerequisites

- AWS Account with Bedrock access
- AWS CLI configured
- Python 3.13+
- Git

### 1. Clone Repository

```bash
git clone https://github.com/higuseonhye/ai-bedrock-chatbot.git
cd ai-bedrock-chatbot
```

### 2. AWS Setup

#### Create Lambda Function
```bash
# Package Lambda function
zip lambda-deployment.zip lambda_function.py

# Create Lambda function (via AWS Console)
# - Runtime: Python 3.13
# - Memory: 512MB
# - Timeout: 30 seconds
```

#### IAM Permissions
Add the following policy to your Lambda execution role:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel"
            ],
            "Resource": "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        }
    ]
}
```

### 3. API Gateway Setup

1. Create REST API
2. Create `/chat` resource with CORS enabled
3. Create POST method with Lambda proxy integration
4. Deploy to `prod` stage

### 4. Deploy to GitHub Pages

1. Fork this repository
2. Enable GitHub Pages in Settings
3. Update `AI_API_URL` in `index.html` with your API Gateway URL
4. Push changes

## 🔧 Configuration

### Update API Endpoint

Edit `index.html` line 263:

```javascript
const AI_API_URL = 'https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com/prod/chat';
```

### Customize AI Model

Edit `lambda_function.py`:

```python
self.model_id = 'anthropic.claude-3-sonnet-20240229-v1:0'  # Change model here
```

## 📁 Project Structure

```
ai-bedrock-chatbot/
├── index.html              # Main chatbot interface
├── ai-chat-webapp.html     # Alternative entry point
├── lambda_function.py      # AWS Lambda handler
├── requirements.txt        # Python dependencies
├── cors_proxy_server.py    # Local development proxy
└── README.md              # This file
```

## 🛠️ Local Development

### With Proxy Server (Recommended)

```bash
# Start CORS proxy server
python3 cors_proxy_server.py

# Open browser
open http://localhost:8000/ai-chat-webapp.html
```

### Direct API Testing

```bash
# Test Lambda function directly
curl -X POST "YOUR_API_GATEWAY_URL/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello from API!"}'
```

## 🎨 Customization

### UI Styling

The chatbot uses modern CSS with:
- Gradient backgrounds
- Smooth animations
- Mobile-responsive design
- Dark/light theme support

### AI Behavior

Modify the AI's behavior in `lambda_function.py`:

```python
request_body = {
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 1000,
    "temperature": 0.7,  # Adjust creativity (0.0-1.0)
    "messages": [{"role": "user", "content": user_message}]
}
```

## 📊 Monitoring

### CloudWatch Logs

Monitor your Lambda function:
- AWS Console → Lambda → Functions → ai-bedrock-agent → Monitor
- View logs for debugging and performance monitoring

### API Gateway Analytics

Track API usage:
- AWS Console → API Gateway → APIs → ai-bedrock-agent-api → Dashboard

## 💰 Cost Estimation

**Monthly costs for moderate usage:**
- AWS Lambda: ~$0.20 (1M requests)
- API Gateway: ~$3.50 (1M requests)
- AWS Bedrock: ~$3.00 (10K tokens/day)
- GitHub Pages: **Free**

**Total: ~$7/month** for significant usage

## 🔒 Security

- ✅ HTTPS everywhere
- ✅ CORS properly configured
- ✅ No API keys exposed in frontend
- ✅ IAM roles with minimal permissions
- ✅ Request/response logging

## 🚀 Performance

- ⚡ **Cold start**: ~2-3 seconds
- ⚡ **Warm requests**: ~500ms
- ⚡ **Global CDN**: <100ms static content
- ⚡ **Auto-scaling**: Handles traffic spikes

## 📱 Mobile Support

Fully responsive design works on:
- 📱 iOS Safari
- 📱 Android Chrome
- 💻 Desktop browsers
- 📟 Tablet devices

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add some amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- AWS Bedrock team for Claude 3 access
- GitHub for free Pages hosting
- Anthropic for the amazing Claude AI model

## 📞 Support

If you have questions or need help:

1. Check the [Issues](https://github.com/higuseonhye/ai-bedrock-chatbot/issues) page
2. Create a new issue with detailed information
3. Join our discussions in the repository

---

**Built with ❤️ using AWS Bedrock Claude 3, API Gateway, Lambda, and GitHub Pages**

[![Deploy to GitHub Pages](https://img.shields.io/badge/Deploy-GitHub%20Pages-blue)](https://docs.github.com/en/pages)
[![AWS Bedrock](https://img.shields.io/badge/Powered%20by-AWS%20Bedrock-orange)](https://aws.amazon.com/bedrock/)

**⭐ Star this repository if you found it helpful!**
