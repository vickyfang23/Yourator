# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 00:37:33 2023

@author: chuan
"""

import scrapy


class YouratorSpider(scrapy.Spider):
    name = 'yourator'
    allowed_domains = ['www.yourator.co']
    start_urls = ['https://www.yourator.co/jobs']

    def parse(self, response):
        # 解析職缺分類列表
        categories = response.css('.category-name::text').getall()

        # 爬取每個職缺分類的職缺資訊
        for category in categories:
            category_url = f'https://www.yourator.co/jobs?category={category}'
            yield scrapy.Request(category_url, callback=self.parse_jobs, meta={'category': category})

    def parse_jobs(self, response):
        category = response.meta['category']

        # 解析職缺列表
        job_list = response.css('.job-card')

        # 爬取每個職缺的詳細資訊
        for job in job_list:
            job_title = job.css('.job-title-link::text').get()
            company_name = job.css('.company-name::text').get()
            job_link = job.css('.job-title-link::attr(href)').get()
            job_url = response.urljoin(job_link)

            # 建立職缺資訊字典
            job_info = {
                '職缺分類': category,
                '公司名稱': company_name,
                '職務名稱': job_title,
                '工作連結': job_url
            }

            # 跟隨職缺連結爬取詳細資訊
            yield scrapy.Request(job_url, callback=self.parse_job_details, meta={'job_info': job_info})

    def parse_job_details(self, response):
        job_info = response.meta['job_info']

        # 解析職缺詳細資訊
        job_description = response.css('.job-description::text').get()
        job_requirements = response.css('.job-requirement::text').get()
        salary_range = response.css('.job-salary::text').get()

        # 更新職缺資訊字典
        job_info['職務描述'] = job_description
        job_info['職務要求'] = job_requirements
        job_info['薪資範圍'] = salary_range

        yield job_info
