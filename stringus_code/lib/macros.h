#ifndef __MACROS_H__
#define __MACROS_H__

#define GET_ARRAY_SIZE(a) (sizeof(a) / sizeof(a[0]))
#define EVER \
    ;        \
    ;
#define FOR_ALL(x) for (uint8_t i = 0; i < GET_ARRAY_SIZE(x); i++)

#define MAX(A, B) (A > B ? A : B)
#define MIN(A, B) (A < B ? A : B)

#define IN_ERROR(VAR, ERROR, GOAL) ((abs(VAR) < (abs(GOAL) + ERROR) && abs(VAR) > (abs(GOAL) - ERROR)))

// Infinite loop
#define BLOCK() for(EVER);

#define __FILENAME__ (strrchr(__FILE__, '/') ? strrchr(__FILE__, '/') + 1 : __FILE__)

enum eLoggerLevel
{
    DEBUG = 10,
    INFO = 20,
    WARN = 30,
    ERROR = 40,
    FATAL = 50
};

#ifdef VERBOSE
// Args: (Logger::eLoggerLevel), (string literal)NodeName, (string literal)format, vars
#define LOG(severity, ...)                                                              \
    if (severity > LOGGER_LOWEST_LEVEL)                                                 \
    {                                                                                   \
        char severityStr[6] = "0_0";                                                    \
        char colorStr[8] = "\033[97m";                                                  \
        switch (severity)                                                               \
        {                                                                               \
        case DEBUG:                                                                     \
            strcpy(severityStr, "DEBUG");                                               \
            break;                                                                      \
                                                                                        \
        case INFO:                                                                      \
            strcpy(severityStr, "INFO");                                                \
            break;                                                                      \
                                                                                        \
        case WARN:                                                                      \
            strcpy(severityStr, "WARN");                                                \
            strcpy(colorStr, "\033[33m");                                               \
            break;                                                                      \
                                                                                        \
        case ERROR:                                                                     \
            strcpy(severityStr, "ERROR");                                               \
            strcpy(colorStr, "\033[31m");                                               \
            break;                                                                      \
                                                                                        \
        case FATAL:                                                                     \
            strcpy(severityStr, "FATAL");                                               \
            strcpy(colorStr, "\033[31m");                                               \
            break;                                                                      \
        }                                                                               \
                                                                                        \
        Serial.printf("%s[%s]%s(%d): ", colorStr, severityStr, __FILENAME__, __LINE__); \
        Serial.printf(__VA_ARGS__);                                                     \
        Serial.printf("\n\033[97m");                                                    \
    }

#else
#define LOG(severity, ...)
#endif // VERBOSE

#endif //__MACROS_H__
