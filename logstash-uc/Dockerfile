ARG ELK_VERSION

FROM logstash:${ELK_VERSION:-7.13.1}

#ADD GeoLite2-City.mmdb /usr/share/GeoIP/

RUN /usr/share/logstash/bin/logstash-plugin install logstash-filter-tld
RUN /usr/share/logstash/bin/logstash-plugin install logstash-input-gelf
RUN /usr/share/logstash/bin/logstash-plugin install logstash-filter-dns

USER 0
RUN yum install -y tcpdump
RUN yum install -y nc
RUN yum install -y epel-release
RUN yum -y update
RUN yum install -y jq
RUN yum clean all
RUN touch /var/log/logs.graylog
RUN touch /var/log/logstash.log
RUN touch /var/log/dgam.log
RUN touch /var/log/elasticsearch.log
RUN chown logstash:root /var/log/logs.graylog
RUN chown logstash:root /var/log/logstash.log
RUN chown logstash:root /var/log/dgam.log
RUN chown logstash:root /var/log/elasticsearch.log

USER 1000

EXPOSE 10000
