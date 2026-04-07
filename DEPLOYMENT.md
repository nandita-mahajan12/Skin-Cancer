# Deployment Checklist & Quick Reference

---

## 🚀 PRE-DEPLOYMENT CHECKLIST

### Code Quality
- [ ] All Python code passes basic checks
- [ ] No console errors in browser developer tools
- [ ] API responds to all test requests
- [ ] Frontend loads successfully
- [ ] Images upload and process correctly
- [ ] Error handling works for invalid inputs

### Security
- [ ] Remove debug mode from Flask: `debug=False`
- [ ] Remove sensitive keys from code
- [ ] CORS properly configured for frontend domain
- [ ] Model file added to .gitignore
- [ ] .env file added to .gitignore
- [ ] No hardcoded passwords or API keys

### Configuration
- [ ] Backend requirements.txt is complete
- [ ] Procfile is correctly formatted
- [ ] vercel.json exists for frontend
- [ ] API_BASE_URL updated for production
- [ ] All imports are available on target platform

### Documentation
- [ ] README.md is complete and accurate
- [ ] API documentation is clear
- [ ] Deployment instructions are tested
- [ ] Troubleshooting section covers common issues
- [ ] Comments added to complex code

---

## 🔧 BACKEND DEPLOYMENT (RENDER)

### Step-by-Step Guide

#### 1. **Prepare Code**
```bash
# Make sure all files are committed
git add .
git commit -m "Prepare for Render deployment"

# Create Procfile (should already exist)
# Contents: web: gunicorn backend.app:app --timeout 300
```

#### 2. **Create Render Account**
- Visit https://render.com
- Sign up (free account)
- Verify email

#### 3. **Create Web Service**
1. Dashboard → New → Web Service
2. **Repository**: Connect GitHub repo (or paste code)
3. **Name**: `skin-cancer-api` (or your choice)
4. **Runtime**: Python 3
5. **Region**: Choose closest to users
6. **Branch**: main
7. **Build Command**: 
   ```
   pip install -r backend/requirements.txt
   ```
8. **Start Command**: 
   ```
   gunicorn backend.app:app --timeout 300
   ```

#### 4. **Set Environment Variables**
In Render Dashboard → Environment:
- `FLASK_ENV`: `production`
- `PYTHON_VERSION`: `3.11`
- Optional: `API_KEY` (for authentication)

#### 5. **Deploy**
- Click "Create Web Service"
- Wait 5-10 minutes
- Verify deployment status
- Copy your API URL: `https://[your-app].onrender.com`

#### 6. **Test Deployment**
```bash
# Test health endpoint
curl https://[your-app].onrender.com/

# Test prediction
curl -X POST -F "image=@test.jpg" https://[your-app].onrender.com/predict
```

### Monitoring
- Dashboard shows logs
- Check "Live logs" for errors
- Monitor "Metrics" for performance

---

## 🎨 FRONTEND DEPLOYMENT (VERCEL)

### Step-by-Step Guide

#### 1. **Update Backend URL**
In `frontend/script.js`:
```javascript
// Change from:
const API_BASE_URL = 'http://localhost:5000';

// To:
const API_BASE_URL = 'https://[your-render-app].onrender.com';
```

#### 2. **Create Vercel Account**
- Visit https://vercel.com
- Sign up with GitHub
- Authorize Vercel

#### 3. **Deploy Frontend**
1. Vercel Dashboard → Add New → Project
2. **Import GitHub Repository** → Select your repo
3. **Project Name**: `skin-cancer-detector` (or your choice)
4. **Framework Preset**: Other
5. **Root Directory**: `frontend/`
6. **Build Settings**: Default (no build needed)

#### 4. **Deploy**
- Click "Deploy"
- Wait 1-2 minutes
- Verify deployment
- Copy your frontend URL: `https://[your-project].vercel.app`

#### 5. **Test Frontend**
1. Open `https://[your-project].vercel.app`
2. Try uploading an image
3. Verify prediction works
4. Check browser console for errors

### Performance Optimization
- Vercel automatically optimizes static assets
- Images are cached at edge locations
- CDN ensures fast delivery globally

---

## 🔗 FULL STACK INTEGRATION

### After Both Deployments

#### 1. **Update Frontend Variables**
In `frontend/script.js`:
```javascript
const API_BASE_URL = 'https://[your-render-app].onrender.com';
```

#### 2. **Update Backend CORS**
In `backend/app.py`:
```python
from flask_cors import CORS

CORS(app, origins=[
    "https://[your-vercel-frontend].vercel.app",
    "http://localhost:8000"  # Keep for local dev
])
```

#### 3. **Redeploy Backend**
```bash
git add backend/app.py
git commit -m "Update CORS for frontend domain"
git push
# Render auto-deploys on push
```

#### 4. **Redeploy Frontend**
```bash
git add frontend/script.js
git commit -m "Update API URL for production"
git push
# Vercel auto-deploys on push
```

#### 5. **Test Full Integration**
1. Open frontend: `https://[your-frontend].vercel.app`
2. Upload image
3. Should connect to backend
4. Get prediction result
5. Should work smoothly

---

## 📊 MONITORING & MAINTENANCE

### Render Backend Monitoring
- **Logs**: Check for errors in live logs
- **Metrics**: Monitor CPU, memory, network
- **Uptime**: Should be 99.9%+
- **Response Time**: Target <5 seconds

### Vercel Frontend Monitoring
- **Analytics**: Track page views, performance
- **Deployment**: Preview each commit
- **Performance**: Check Lighthouse scores
- **Uptime**: Should be 99.99%+

### Regular Maintenance
- [ ] Monthly review of logs
- [ ] Update dependencies quarterly
- [ ] Monitor API error rates
- [ ] Check model serving performance
- [ ] Review cost estimates

---

## 💰 ESTIMATED COSTS

### Render (Backend)
- **Free Tier**: 1 free instance, limited memory
- **Starter Plan**: $7/month
- **Cost Factors**: 
  - Model file size
  - Number of predictions
  - Response time

### Vercel (Frontend)
- **Free Tier**: 100GB bandwidth/month
- **Pro Plan**: $20/month
- **Cost Factor**: Bandwidth usage

### Total Estimated Cost
- **Development**: $0 (free tier)
- **Small Production**: $15-30/month
- **Medium Production**: $50-100/month

---

## 🔒 SECURITY BEST PRACTICES

### Before Production
1. **Disable Debug Mode**
   ```python
   app.run(debug=False, host='0.0.0.0', port=5000)
   ```

2. **Set Secret Key**
   ```python
   app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
   ```

3. **Use HTTPS** (automatic on Render/Vercel)

4. **Validate All Inputs** (already done)

5. **Rate Limiting** (optional)
   ```python
   from flask_limiter import Limiter
   limiter = Limiter(app)
   ```

6. **CORS Security**
   ```python
   CORS(app, origins=['https://your-domain.com'])
   ```

### Secrets Management
- Never commit API keys
- Use environment variables
- Rotate keys periodically
- Monitor access logs

---

## 🚨 TROUBLESHOOTING DEPLOYMENT

### Issue: Deployment Failed
```
Solutions:
1. Check build logs for errors
2. Verify requirements.txt is correct
3. Test locally first
4. Check file paths
5. Ensure Procfile is correct
```

### Issue: 504 Gateway Timeout
```
Solutions:
1. Model loading takes too long
2. Increase timeout: --timeout 300
3. Optimize model loading
4. Use GPU instance
5. Cache model in memory
```

### Issue: Out of Memory
```
Solutions:
1. Upgrade to paid tier
2. Quantize model (reduce size)
3. Use TensorFlow Lite
4. Implement caching
5. Reduce batch size
```

### Issue: CORS Error
```
Solutions:
1. Check CORS configuration
2. Verify frontend URL
3. Check browser console
4. Test with curl
5. Check preflight requests
```

### Issue: Model File Too Large
```
Solutions:
1. Use model.tflite (quantized)
2. Use ONNX format
3. Cloud storage (Firebase, S3)
4. Model compression
5. Use model zoo
```

---

## 📈 SCALING FOR PRODUCTION

### For More Users
1. **Upgrade Render Tier**
   - Standard plan: $7+/month
   - Professional plan: $25+/month

2. **Use Load Balancer**
   - Render provides automatic load balancing

3. **Implement Caching**
   - Cache model in memory
   - Cache predictions temporarily

4. **Database (Optional)**
   - Store user predictions
   - Track analytics
   - MongoDB or PostgreSQL

### For Better Performance
1. **Model Optimization**
   - Quantization
   - Pruning
   - Knowledge distillation

2. **Use GPU**
   - For faster predictions
   - NVIDIA GPUs available

3. **Async Processing**
   - Queue predictions
   - Background jobs

4. **CDN for Images**
   - Cloudflare
   - AWS CloudFront

---

## 📝 POST-DEPLOYMENT TASKS

### Week 1
- [ ] Monitor logs hourly
- [ ] Test with real users
- [ ] Gather feedback
- [ ] Fix critical issues
- [ ] Document issues found

### Month 1
- [ ] Review analytics
- [ ] Optimize performance
- [ ] Update documentation
- [ ] Plan improvements
- [ ] Monitor costs

### Ongoing
- [ ] Monthly security checks
- [ ] Update dependencies (quarterly)
- [ ] Monitor performance metrics
- [ ] Backup data regularly
- [ ] Plan for scaling

---

## 📞 GETTING HELP

### Resources
- Render Docs: https://render.com/docs
- Vercel Docs: https://vercel.com/docs
- Flask Docs: https://flask.palletsprojects.com/
- TensorFlow Docs: https://www.tensorflow.org/

### Support Channels
- Render Support: https://support.render.com
- Vercel Support: https://vercel.com/support
- Stack Overflow: Tag `flask`, `tensorflow`
- GitHub Issues: Your repo issues section

---

## ✅ Deployment Verification Checklist

After deployment, verify:
- [ ] Frontend loads without errors
- [ ] API responds to health check
- [ ] Can upload image from frontend
- [ ] Prediction returns correct format
- [ ] Confidence scores are reasonable
- [ ] Error messages display properly
- [ ] Page loads within 3 seconds
- [ ] Images upload within 10 seconds
- [ ] Prediction returns within 5 seconds
- [ ] Mobile responsive design works
- [ ] No CORS errors
- [ ] No 404 errors
- [ ] HTTPS is enforced
- [ ] Performance is acceptable

---

**Congratulations! 🎉 Your app is deployed and live!**

Share the link and start helping people with skin cancer detection!
