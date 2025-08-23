# Deployment Guide - Fix for Disappearing Event Images

## Problem
Event images are disappearing on Heroku after some time because:
- Heroku has an ephemeral filesystem
- Files uploaded to the server are lost when dynos restart
- The current upload path conflicts with static file serving

## Solution
Use cloud storage for media files instead of local storage.

## Option 1: Cloudinary (Recommended - Free Tier Available)

### 1. Sign up for Cloudinary
- Go to [cloudinary.com](https://cloudinary.com)
- Create a free account
- Get your cloud name, API key, and API secret

### 2. Set Environment Variables on Heroku
```bash
heroku config:set CLOUDINARY_CLOUD_NAME=ddkeblfid
heroku config:set CLOUDINARY_API_KEY=761662694724374
heroku config:set CLOUDINARY_API_SECRET=yPNuK2ZZ4T4_QfDt1n_-_OWh7J8
```

### 3. Deploy
```bash
git add .
git commit -m "Add cloud storage for media files"
git push heroku main
```

## Option 2: AWS S3 (Requires AWS Account)

### 1. Create S3 Bucket
- Create an S3 bucket in AWS
- Set it to public (for media files)
- Get your access keys

### 2. Set Environment Variables
```bash
heroku config:set AWS_ACCESS_KEY_ID=your_access_key
heroku config:set AWS_SECRET_ACCESS_KEY=your_secret_key
heroku config:set AWS_STORAGE_BUCKET_NAME=your_bucket_name
heroku config:set AWS_S3_REGION_NAME=us-east-1
```

### 3. Uncomment S3 Configuration
In `Fgen_New/settings.py`, uncomment the AWS S3 section and comment out Cloudinary.

## Option 3: Quick Fix (Temporary)

If you want a quick fix without cloud storage:

### 1. Create Media Directory
```bash
mkdir media
mkdir media/images
mkdir media/pdfs
```

### 2. Add to .gitignore
```
media/
```

### 3. Manual Upload After Each Deploy
After each Heroku deploy, manually re-upload your images through the admin panel.

## Testing

1. Upload an image through the admin panel
2. Check if it appears on your events page
3. Restart your Heroku dyno: `heroku restart`
4. Check if the image still appears

## Important Notes

- **Cloudinary Free Tier**: 25 GB storage, 25 GB bandwidth/month
- **AWS S3**: Pay per use, very cheap for small sites
- **Local Storage**: Only works in development, not production

## Recommended Approach

1. Start with Cloudinary (free, easy setup)
2. Move to AWS S3 if you need more storage/bandwidth
3. Never rely on local storage for production media files

## Troubleshooting

If images still don't appear:
1. Check your environment variables are set correctly
2. Verify the storage backend is working
3. Check the media URL in your templates
4. Ensure proper file permissions on your cloud storage
