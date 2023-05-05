.PHONY: maptools
requires:
	sudo apt-get install graphviz
	sudo apt-get install xdg-utils
	pip3 install -U -r requirements.txt

maptools:
	python3 setup.py build_ext --inplace
	sudo python3 setup.py install

.PHONY: clean

clean:
	rm -rf ./dist
	rm -rf ./build
