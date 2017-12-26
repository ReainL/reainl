-- 新闻表
DROP TABLE IF EXISTS public.news_cj;
CREATE TABLE public.news_cj(
    news_date character varying(20),
    spider_data timestamp,
    news_source text,
    news_type text,
    news text
);
COMMENT ON TABLE public.news_cj IS '新闻表';
COMMENT ON COLUMN public.news_cj.news_date IS '新闻日期';
COMMENT ON COLUMN public.news_cj.spider_data IS '操作时间';
COMMENT ON COLUMN public.news_cj.news_source IS '新闻来源';
COMMENT ON COLUMN public.news_cj.news_type IS '新闻类型';
COMMENT ON COLUMN public.news_cj.news IS '新闻内容';

-- 美元指数表
DROP TABLE IF EXISTS public.stock_code;
CREATE TABLE public.stock_code (
    stock_time character(20),
    spider_data timestamp,
    stock_name bpchar(5) NULL,
    stock_price numeric(5,4) NULL,
    stock_applies numeric(5,4) NULL
);
COMMENT ON TABLE public.stock_code IS '美元指数表';
COMMENT ON COLUMN public.stock_code.stock_time IS '行情时间';
COMMENT ON COLUMN public.stock_code.spider_data IS '操作时间';
COMMENT ON COLUMN public.stock_code.stock_name IS '指数名称';
COMMENT ON COLUMN public.stock_code.stock_price IS '指数价格';
COMMENT ON COLUMN public.stock_code.stock_applies IS '涨跌幅';

insert into public.stock_code(
    stock_time, spider_data, stock_name, stock_price)
values('2017-12-25 15:40:17', '2017-12-25 15:40:17', '人民币汇率', '6.576');