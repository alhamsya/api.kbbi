from core.hooks import resp_err


def error_handler(app):

    @app.errorhandler(403)
    def forbidden(err):
        return resp_err(str(err), 1, 403)

    @app.errorhandler(404)
    def page_not_found(err):
        return resp_err("Not Found", 2, 404)

    @app.errorhandler(405)
    def method_not_allowed(err):
        return resp_err("No Access Allowed", 3, 405)

    @app.errorhandler(500)
    def internal_server_error(err):
        return resp_err("Internal server error", 4, 500)
