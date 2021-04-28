from setuptools import setup

setup(
    name='ask-the-duck',
    version='0.0.1',
    packages=['ask_the_duck'],
    url='https://github.com/HelloChatterbox/ask-the-duck',
    license='apache-2.0',
    author='jarbasAi',
    install_requires=["requests",
                      "requests_cache",
                      "google_trans_new",
                      "quebra_frases",
                      "RAKEkeywords",
                      "simplematch"],
    author_email='jarbasai@mailfence.com',
    description='duck duck go library'
)
