# Resend
Resend is a script who ingest logs using Filebeat to Logstash 

# Example usage
```bash
docker run \
-v $(PWD)/input.log:/input.log \
-v /etc/pki/tls/somecert.crt:/cert.crt \
-ti p404/resend
```
