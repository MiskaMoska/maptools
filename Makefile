.PHONY: maptools
requires:
	sudo apt-get install graphviz
	sudo apt-get install xdg-utils
	pip3 install -U -r requirements.txt

maptools:
	sudo python3 setup.py install

.PHONY: clean
clean:
	rm -rf ./build
	rm -rf ./mapsave
