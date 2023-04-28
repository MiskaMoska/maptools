# VCS
COMPILER = vcs -full64 -cc gcc-4.8 -cpp g++-4.8 -LDFLAGS -Wl,-no-as-needed
TOP_MODLE = -top top_tb
TIMESCALE = -timescale=1ns/1ps
INCDIR = +incdir+../config/network_config

# Verdi
PLI_TAB = $(VERDI_HOME)/share/PLI/VCS/LINUXAMD64/novas.tab
PLI_A = $(VERDI_HOME)/share/PLI/VCS/LINUXAMD64/pli.a
FSDB = -fsdb -P $(PLI_TAB) $(PLI_A)

run:
	$(COMPILER)	-sverilog -f filelist.f  \
	$(TOP_MODULE)   					 \
	$(TIMESCALE)						 \
	$(INCDIR)						     \
	$(FSDB)
	./simv

verdi:
	verdi +v2k -sverilog $(INCDIR) -f filelist.f -ssf wave.fsdb -sswr cfg1.r


.PHONY:clean
clean:
	rm -rf simv.daidir csrc verdiLog novas* simv ucli.key 
	rm -rf receive_pool*
	rm -rf wave.*
	rm -rf *.fsdb
	rm -rf ../log/*.log