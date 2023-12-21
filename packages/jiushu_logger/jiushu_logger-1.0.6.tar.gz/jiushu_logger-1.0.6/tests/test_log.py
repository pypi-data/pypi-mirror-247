# coding: utf-8
import logging
from unittest import TestCase

from jiushu_logger.log import *


class TestLogging(TestCase):
    def test_biz_logging(self):
        with self.assertLogs(Logger.biz, level=logging.DEBUG) as captured:
            Logger.biz.info('biz info', extra=BizLogExtra())
            Logger.biz.debug('biz debug', extra=BizLogExtra(trace_id='biz-001'))
            Logger.biz.warning('biz warning', extra=BizLogExtra(duration=32))
            Logger.biz.error('biz error', extra=BizLogExtra(trace_id='biz-003', duration=1.23456))

        records = captured.records
        self.assertEqual(len(records), 4)
        self.assertTrue(all(record.name == 'jf_service_biz' for record in records))
        self.assertTrue(all(record.cate == 'biz' for record in records))

        self.assertIsNone(records[0].trace_id)
        self.assertIsNone(records[0].duration)

        self.assertEqual(records[1].trace_id, 'biz-001')
        self.assertIsNone(records[1].duration)

        self.assertIsNone(records[2].trace_id)
        self.assertTrue(isinstance(records[2].duration, int))
        self.assertEqual(records[2].duration, 32000)

        self.assertEqual(records[3].trace_id, 'biz-003')
        self.assertTrue(isinstance(records[3].duration, int))
        self.assertEqual(records[3].duration, 1234)

    def test_req_logging(self):
        with self.assertLogs(Logger.req, level=logging.DEBUG) as captured:
            Logger.req.info('req info', extra=ReqLogExtra())
            Logger.req.info('req info', extra=ReqLogExtra(duration=1.23456,
                                                          method='GET',
                                                          path='/path',
                                                          client_ip='1.2.3.4',
                                                          host='5.6.7.8',
                                                          headers='a',
                                                          query='b',
                                                          body='c',
                                                          resp='d'))

        records = captured.records
        self.assertEqual(len(records), 2)
        self.assertTrue(all(record.name == 'jf_service_req' for record in records))
        self.assertTrue(all(record.cate == 'req' for record in records))

        self.assertIsNone(records[0].method)
        self.assertIsNone(records[0].path)
        self.assertIsNone(records[0].client_ip)
        self.assertIsNone(records[0].host)
        self.assertIsNone(records[0].headers)
        self.assertIsNone(records[0].query)
        self.assertIsNone(records[0].body)
        self.assertIsNone(records[0].resp)

        self.assertTrue(isinstance(records[1].duration, int))
        self.assertEqual(records[1].duration, 1234)
        self.assertEqual(records[1].method, 'GET')
        self.assertEqual(records[1].path, '/path')
        self.assertEqual(records[1].client_ip, '1.2.3.4')
        self.assertEqual(records[1].host, '5.6.7.8')
        self.assertEqual(records[1].headers, 'a')
        self.assertEqual(records[1].query, 'b')
        self.assertEqual(records[1].body, 'c')
        self.assertEqual(records[1].resp, 'd')

    def test_call_logging(self):
        with self.assertLogs(Logger.call, level=logging.DEBUG) as captured:
            Logger.call.info('call info', extra=CallLogExtra(type=CallType.INTERN))
            Logger.call.info('call info', extra=CallLogExtra(type=CallType.EXTERN))
            Logger.call.info('call info', extra=CallLogExtra(type=CallType.INTERN,
                                                             params={'i1': 'iv1'},
                                                             resp={'o1': 'ov1', 'o2': 'ov2'}))

        records = captured.records
        self.assertEqual(len(records), 3)
        self.assertTrue(all(record.name == 'jf_service_call' for record in records))

        self.assertEqual(records[0].cate, CallType.INTERN.value)
        self.assertIsNone(records[0].call_params)
        self.assertIsNone(records[0].call_resp)

        self.assertEqual(records[1].cate, CallType.EXTERN.value)
        self.assertIsNone(records[1].call_params)
        self.assertIsNone(records[1].call_resp)

        self.assertEqual(records[2].cate, CallType.INTERN.value)
        self.assertEqual(records[2].call_params, '{"i1":"iv1"}')
        self.assertEqual(records[2].call_resp, '{"o1":"ov1","o2":"ov2"}')

    def test_cron_logging(self):
        with self.assertLogs(Logger.cron, level=logging.DEBUG) as captured:
            Logger.cron.info('cron info', extra=CronLogExtra())
            Logger.cron.info('cron info', extra=CronLogExtra(job_group='group', job_code='code'))

        records = captured.records
        self.assertEqual(len(records), 2)
        self.assertTrue(all(record.name == 'jf_service_cron' for record in records))
        self.assertTrue(all(record.cate == 'cron' for record in records))

        self.assertIsNone(records[0].job_group)
        self.assertIsNone(records[0].job_code)

        self.assertEqual(records[1].job_group, 'group')
        self.assertEqual(records[1].job_code, 'code')

    def test_middleware_logging(self):
        with self.assertLogs(Logger.middleware, level=logging.DEBUG) as captured:
            Logger.middleware.info('middleware info', extra=MiddlewareLogExtra(type=MiddlewareType.MYSQL))
            Logger.middleware.info('middleware info', extra=MiddlewareLogExtra(type=MiddlewareType.MONGO))
            Logger.middleware.info('middleware info', extra=MiddlewareLogExtra(type=MiddlewareType.REDIS))
            Logger.middleware.info('middleware info', extra=MiddlewareLogExtra(type=MiddlewareType.ES))
            Logger.middleware.info('middleware info',
                                   extra=MiddlewareLogExtra(type=MiddlewareType.ES, host='1.2.3.4'))

        records = captured.records
        self.assertEqual(len(records), 5)
        self.assertTrue(all(record.name == 'jf_service_middleware' for record in records))

        self.assertEqual(records[0].cate, MiddlewareType.MYSQL.value)
        self.assertIsNone(records[0].host)

        self.assertEqual(records[1].cate, MiddlewareType.MONGO.value)

        self.assertEqual(records[2].cate, MiddlewareType.REDIS.value)

        self.assertEqual(records[3].cate, MiddlewareType.ES.value)

        self.assertEqual(records[4].host, '1.2.3.4')

    def test_mq_logging(self):
        with self.assertLogs(Logger.mq, level=logging.DEBUG) as captured:
            Logger.mq.info('mq info', extra=MqLogExtra(type=MqType.MQ, handle_type=MqHandleType.SEND))
            Logger.mq.info('mq info', extra=MqLogExtra(type=MqType.MQTT, handle_type=MqHandleType.SEND))
            Logger.mq.info('mq info', extra=MqLogExtra(type=MqType.KAFKA, handle_type=MqHandleType.SEND))
            Logger.mq.info('mq info', extra=MqLogExtra(type=MqType.KAFKA, handle_type=MqHandleType.SEND))
            Logger.mq.info('mq info', extra=MqLogExtra(type=MqType.KAFKA, handle_type=MqHandleType.LISTEN))

        records = captured.records
        self.assertEqual(len(records), 5)
        self.assertTrue(all(record.name == 'jf_service_mq' for record in records))

        self.assertEqual(records[0].cate, MqType.MQ.value)

        self.assertEqual(records[1].cate, MqType.MQTT.value)

        self.assertEqual(records[2].cate, MqType.KAFKA.value)

        self.assertEqual(records[3].cate, MqType.KAFKA.value)
        self.assertEqual(records[3].handle, MqHandleType.SEND.value)

        self.assertEqual(records[4].handle, MqHandleType.LISTEN.value)
