import setuptools

setuptools.setup(
	name='claude_2_api',
	version='1.0.0',
	author='__token__',
	author_email='aleksfolt@ya.ru',
	description='Claude api with the new 2.1 model referring to a non-working repo: https://github.com/KoushikNavuluri/Claude-API',
	url='https://github.com/aleksfolt/claude-2-api',
	packages=['Claude2Api'],
	include_package_data=True,
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.6',
)