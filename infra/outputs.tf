output "alb_dns_name" {
  value = aws_lb.main.dns_name
}

output "cloudfront_domain" {
  value = aws_cloudfront_distribution.frontend.domain_name
}

output "dashboard_url" {
  value = "https://dashboard.kevinlutes.com"  
}

output "api_url" {
  value = "https://api.kevinlutes.com"  
}