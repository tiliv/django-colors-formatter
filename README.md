# django-colors-formatter

Zero-config logging formatter that uses the built-in DJANGO_COLORS setting

## Setup

In your Django `LOGGING` settings, just add this to your formatters, and then reference it in (for example) a console logger:

    LOGGING = {
        'formatters': {
            'colored': {
                '()': 'djangocolors_formatter.DjangoColorsFormatter',
                'format': '%(levelname)s %(module)s %(message)s',
            },
        },
        'handlers': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'colored',
        },
        'loggers': 
            'myproject': {
                'handlers': ['console'],
                'level': 'DEBUG',
            },
        },    
    }

The formatter generates its colors with Django's own internal colorizing mechanism, which means that the [`DJANGO_COLORS`](https://docs.djangoproject.com/en/dev/ref/django-admin/#syntax-coloring) environment variable is respected.

`DjangoColorsFormatter` maps Django's default HTTP status code colors to the built-in logging levels:

* DEBUG = `HTTP_NOT_MODIFIED` (light=green; dark=cyan)
* INFO = `HTTP_INFO` (plain/bold)
* WARNING = `HTTP_NOT_FOUND` (light=red; dark=yellow)
* ERROR = `ERROR` (red/bold)
* CRITICAL = `HTTP_SERVER_ERROR` (magenta/bold)

## Environment variable: simple configuration

Django lets you configure these values, as described [here](https://docs.djangoproject.com/en/dev/ref/django-admin/#syntax-coloring), but due to the way their palette generation works, you can't invent your own logging names.  That is, if you want to change the `WARNING` color, you indeed have to set your environment variable to use an `HTTP_NOT_FOUND` color, which this formatting class will pull over for its own use.

## Subclassing the formatter: free-form configuration

By subclassing the formatter, you can override the custom `configure_style()` method, which does the default color assignments.

    def configure_style(self, style):
        style.DEBUG = style.HTTP_NOT_MODIFIED
        style.INFO = style.HTTP_INFO
        style.WARNING = style.HTTP_NOT_FOUND
        style.ERROR = style.ERROR
        style.CRITICAL = style.HTTP_SERVER_ERROR
        return style

`style` is just a dummy object that you assign arbitrary attributes to.  At runtime, the logging level name is looked up.

The attributes should be dictionaries, which define color options using the same environment variable names.  For example, the Django documentation gives the following demonstration of setting the `DJANGO_COLORS` variable:

    export DJANGO_COLORS="error=yellow/blue,blink;notice=magenta"

This would set "ERROR" messages in blinking yellow on blue, and "NOTICE" messages in magenta foreground.

To accomplish this in a formatting subclass, you would do the following:

    def configure_style(self, style):
        style.ERROR = {
            'fg': 'yellow',
            'bg': 'blue',
            'opts': ('blink',),
        }
        style.NOTICE = {
            'fg': 'magenta',
        }

This is the formatting design used internally by Django to set the default color palettes.

To stylize a custom logging level name, you must use this subclassing method and assign that name a configuration dictionary (shown just above), or assign one of the default style names from the built-in palette.
