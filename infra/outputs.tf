output "alb_dns_name" {
  description = "ALB DNS name - internal use only, not exposed publicly"
  value       = aws_lb.main.dns_name
}

output "cloudfront_domain" {
  description = "CloudFront distribution domain"
  value       = aws_cloudfront_distribution.frontend.domain_name
}

output "dashboard_url" {
  description = "Live dashboard URL"
  value       = "https://dashboard.kevinlutes.com"
}
