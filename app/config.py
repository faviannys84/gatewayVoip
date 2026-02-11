# Configuration Settings

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'

class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URI = os.environ.get('DEV_DATABASE_URI')

class ProductionConfig(Config):
    DEBUG = False
    DATABASE_URI = os.environ.get('DATABASE_URI')

# Dictionary to easily switch configurations
configurations = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
