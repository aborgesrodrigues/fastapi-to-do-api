from to_do_api.audit_logging.http_audit_logger import HTTPAuditLogger

audit_logger = HTTPAuditLogger.from_env()
audit_logger.start()