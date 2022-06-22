FROM public.ecr.aws/amazonlinux/amazonlinux:2022

COPY /gotty /gotty
COPY /run_gotty.sh /run_gotty.sh

RUN chmod 744 /gotty
RUN chmod 744 /run_gotty.sh

EXPOSE 8080

CMD ["/run_gotty.sh"]