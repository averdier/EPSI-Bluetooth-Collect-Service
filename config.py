# -*- coding: utf-8 -*-


class Config:
    """
    Base configuration
    """

    MQTT_SERVER = "93.118.34.190"
    MQTT_PORT = 1883
    MQTT_USERNAME = "triangulation_service"
    MQTT_TOKEN = "Viyywn1hMyME83yM"
    MQTT_KEEP_ALIVE = 60


class DevelopmentConfig(Config):
    """
    Development configuration
    """


class ProductionConfig(Config):
    """
    Production configuration
    """


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
