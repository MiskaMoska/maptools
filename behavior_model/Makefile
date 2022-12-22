COMPILER = vcs -full64 -cc gcc-4.8 -cpp g++-4.8 -LDFLAGS -Wl,-no-as-needed
TOP_MODLE = -top cast_router
INCDIR = +incdir+./srcs

comp:
	$(COMPILER)	-sverilog -f filelist.f  \
	$(TOP_MODULE)   					 \
	$(INCDIR)
