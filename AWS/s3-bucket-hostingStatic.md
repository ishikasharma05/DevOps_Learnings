# Hosting My Portfolio on AWS S3 (Static Website Hosting)

As part of my AWS learning journey (IAM, EC2, S3, MFA, VPC), I deployed my personal portfolio website using **S3 Static Website Hosting**. This document covers what the service is, the steps I followed, the role of the bucket policy, the live URL, and what I'd do next to make this production-grade.

---

## 1. What is S3 Static Website Hosting?

S3 Static Website Hosting is a feature of Amazon S3 that lets you serve static files (HTML, CSS, JavaScript, images) directly from a bucket over HTTP — without needing a traditional web server like Apache or Nginx, and without spinning up a compute instance (EC2).

When enabled, S3 assigns the bucket a website endpoint URL. Any request to that URL is served directly from the objects stored in the bucket, with S3 handling things like:
- Serving a specified **index document** (e.g. `index.html`) for the root path
- Serving a specified **error document** (e.g. `error.html`) for 404s
- Returning files with correct content types based on their extension

It's commonly used for portfolios, landing pages, and single-page apps — anything that doesn't need server-side logic (no backend, no database).
<img width="491" height="61" alt="image" src="https://github.com/user-attachments/assets/510b5364-1d84-4e0a-a657-faee2c8983aa" />

---

## 2. Steps I Followed

1. **Created an S3 bucket** with a globally unique name, in my chosen AWS region.
2. **Uploaded my portfolio files** (`index.html`, CSS, JS, images, etc.) to the bucket.
3. **Enabled Static Website Hosting** under the bucket's *Properties* tab, and specified:
   - Index document: `index.html`
   - Error document: `error.html` (if configured)
4. **Disabled "Block all public access"** at the bucket level — by default S3 blocks public access, and this has to be turned off before a public bucket policy can take effect.
5. **Attached a bucket policy** (see below) to allow public read access to the objects.
6. **Verified the site** by visiting the S3 website endpoint URL generated under the Static Website Hosting section.

> *Note: fill in or correct any step above based on the exact order you performed them in — e.g. if you uploaded files after enabling hosting, or configured the policy before uploading.*

---

## 3. What the Bucket Policy Was For

By default, **every S3 bucket is private** — even after enabling static website hosting, visitors would get an "Access Denied" error without explicit permission to read the files.

A **bucket policy** is a JSON-based access control document attached to the bucket. It explicitly defines:
- **Who** can access the bucket (the `Principal`)
- **What actions** they're allowed to perform (e.g. `s3:GetObject`)
- **Which resources** the permission applies to (e.g. all objects in the bucket)

For public static hosting, the policy I attached granted `s3:GetObject` permission to everyone (`"Principal": "*"`) on all objects in the bucket. This is what allows any visitor's browser to fetch and render the files — without it, the site would be unreachable even with hosting "enabled."

Example of the kind of policy used:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::YOUR-BUCKET-NAME/*"
    }
  ]
}
```

This keeps access scoped to **read-only on objects** — visitors can view files, but can't list, upload, modify, or delete anything in the bucket.

---

## 4. Live URL

**Live site:** `[PASTE YOUR S3 WEBSITE ENDPOINT URL HERE]`

*(Found under your bucket → Properties → Static website hosting → "Bucket website endpoint." It typically looks like `http://your-bucket-name.s3-website-<region>.amazonaws.com`.)*

<img width="334" height="67" alt="image" src="https://github.com/user-attachments/assets/8a442f9d-8280-475d-8908-07a5ea54bfbe" />

<img width="956" height="491" alt="image" src="https://github.com/user-attachments/assets/5bf180ca-6f7e-4e28-a1f9-6913980facb8" />

---

## 5. Next Steps for Production Grade

S3 static hosting alone is a great starting point, but it has real limitations: no HTTPS, no custom domain, no caching/CDN, and no protection against accidental public bucket misconfiguration. To take this further, I'd plan to:

- **Add CloudFront (CDN)** — distributes content globally, reduces latency, and is required to enable HTTPS in front of an S3 static site.
- **Enable HTTPS via AWS Certificate Manager (ACM)** — S3 website endpoints don't support HTTPS natively; this comes through CloudFront + ACM.
- **Use a custom domain with Route 53** — point a real domain (e.g. `ishikasharma.dev`) to the CloudFront distribution instead of the raw S3 URL.
- **Enable S3 versioning** — protects against accidental overwrites or deletions of site files.
- **Enable access logging** — track requests for visibility and basic analytics.
- **Set up CI/CD for deployment** — e.g. GitHub Actions to auto-sync the `dist`/build folder to S3 on every push, instead of manual uploads.
- **Review the bucket policy regularly** — confirm it's scoped to only what's needed (`GetObject` on objects, not broader permissions).

---

## Stack / Learning Context

This project was built while learning core AWS services: **IAM, EC2, S3, MFA, and VPC.** It served as a hands-on introduction to real cloud deployment, complementing the conceptual study of the AWS ecosystem.
