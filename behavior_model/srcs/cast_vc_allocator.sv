`include "params.svh"

module cast_vc_allocator (
    input       wire                            clk,
    input       wire                            rstn,

    //VC req from input ports
    input       wire        [`CN-1:0]           reqVCfromVC0, 
    input       wire        [`CN-1:0]           reqVCfromVC1, 
    input       wire        [`CN-1:0]           reqVCfromVC2, 
    input       wire        [`CN-1:0]           reqVCfromVC3, 
    input       wire        [`CN-1:0]           reqVCfromVC4, 

    //VC availability from output ports
    input       wire        [`CN-1:0]           outVCAvailable,

    //VC selected to input ports 
    output      wire        [`CN-1:0]           selOutVCtoVC0,
    output      wire        [`CN-1:0]           selOutVCtoVC1,
    output      wire        [`CN-1:0]           selOutVCtoVC2,
    output      wire        [`CN-1:0]           selOutVCtoVC3,
    output      wire        [`CN-1:0]           selOutVCtoVC4,

    //VC grant signal to input ports
    output      wire        [`CN-1:0]           VCgranted,     

    //inform the outVCAvailable when to reset
    output      wire        [`CN-1:0]           outVCAvailableReset                       
);

wire [`CN-1:0] reqMaskedVCfromVC0;
wire [`CN-1:0] reqMaskedVCfromVC1;
wire [`CN-1:0] reqMaskedVCfromVC2;
wire [`CN-1:0] reqMaskedVCfromVC3;
wire [`CN-1:0] reqMaskedVCfromVC4;

assign reqMaskedVCfromVC0 = reqVCfromVC0 & outVCAvailable;
assign reqMaskedVCfromVC1 = reqVCfromVC1 & outVCAvailable;
assign reqMaskedVCfromVC2 = reqVCfromVC2 & outVCAvailable;
assign reqMaskedVCfromVC3 = reqVCfromVC3 & outVCAvailable;
assign reqMaskedVCfromVC4 = reqVCfromVC4 & outVCAvailable;

wire [`CN-1:0] arb_req_to_VC0,arb_grt_from_VC0;
wire [`CN-1:0] arb_req_to_VC1,arb_grt_from_VC1;
wire [`CN-1:0] arb_req_to_VC2,arb_grt_from_VC2;
wire [`CN-1:0] arb_req_to_VC3,arb_grt_from_VC3;
wire [`CN-1:0] arb_req_to_VC4,arb_grt_from_VC4;

assign arb_req_to_VC0 = {reqMaskedVCfromVC4[0],reqMaskedVCfromVC3[0],reqMaskedVCfromVC2[0],reqMaskedVCfromVC1[0],reqMaskedVCfromVC0[0]};
assign arb_req_to_VC1 = {reqMaskedVCfromVC4[1],reqMaskedVCfromVC3[1],reqMaskedVCfromVC2[1],reqMaskedVCfromVC1[1],reqMaskedVCfromVC0[1]};
assign arb_req_to_VC2 = {reqMaskedVCfromVC4[2],reqMaskedVCfromVC3[2],reqMaskedVCfromVC2[2],reqMaskedVCfromVC1[2],reqMaskedVCfromVC0[2]};
assign arb_req_to_VC3 = {reqMaskedVCfromVC4[3],reqMaskedVCfromVC3[3],reqMaskedVCfromVC2[3],reqMaskedVCfromVC1[3],reqMaskedVCfromVC0[3]};
assign arb_req_to_VC4 = {reqMaskedVCfromVC4[4],reqMaskedVCfromVC3[4],reqMaskedVCfromVC2[4],reqMaskedVCfromVC1[4],reqMaskedVCfromVC0[4]};

mtx_arbiter #(
    .LEN                   (`CN)
)arbiterVC0(
    .clk                   (clk),
    .rstn                  (rstn),
    .request               (arb_req_to_VC0),
    .grant                 (arb_grt_from_VC0),
    .update                (1'b1)
);

mtx_arbiter #(
    .LEN                   (`CN)
)arbiterVC1(
    .clk                   (clk),
    .rstn                  (rstn),
    .request               (arb_req_to_VC1),
    .grant                 (arb_grt_from_VC1),
    .update                (1'b1)
);

mtx_arbiter #(
    .LEN                   (`CN)
)arbiterVC2(
    .clk                   (clk),
    .rstn                  (rstn),
    .request               (arb_req_to_VC2),
    .grant                 (arb_grt_from_VC2),
    .update                (1'b1)
);

mtx_arbiter #(
    .LEN                   (`CN)
)arbiterVC3(
    .clk                   (clk),
    .rstn                  (rstn),
    .request               (arb_req_to_VC3),
    .grant                 (arb_grt_from_VC3),
    .update                (1'b1)
);

mtx_arbiter #(
    .LEN                   (`CN)
)arbiterVC4(
    .clk                   (clk),
    .rstn                  (rstn),
    .request               (arb_req_to_VC4),
    .grant                 (arb_grt_from_VC4),
    .update                (1'b1)
);

assign selOutVCtoVC0 = {arb_grt_from_VC4[0],arb_grt_from_VC3[0],arb_grt_from_VC2[0],arb_grt_from_VC1[0],arb_grt_from_VC0[0]};
assign selOutVCtoVC1 = {arb_grt_from_VC4[1],arb_grt_from_VC3[1],arb_grt_from_VC2[1],arb_grt_from_VC1[1],arb_grt_from_VC0[1]};
assign selOutVCtoVC2 = {arb_grt_from_VC4[2],arb_grt_from_VC3[2],arb_grt_from_VC2[2],arb_grt_from_VC1[2],arb_grt_from_VC0[2]};
assign selOutVCtoVC3 = {arb_grt_from_VC4[3],arb_grt_from_VC3[3],arb_grt_from_VC2[3],arb_grt_from_VC1[3],arb_grt_from_VC0[3]};
assign selOutVCtoVC4 = {arb_grt_from_VC4[4],arb_grt_from_VC3[4],arb_grt_from_VC2[4],arb_grt_from_VC1[4],arb_grt_from_VC0[4]};

assign VCgranted[0] = (arb_grt_from_VC0[0] | arb_grt_from_VC1[0] | arb_grt_from_VC2[0] | arb_grt_from_VC3[0] | arb_grt_from_VC4[0]) & (reqVCfromVC0 == selOutVCtoVC0); 
assign VCgranted[1] = (arb_grt_from_VC0[1] | arb_grt_from_VC1[1] | arb_grt_from_VC2[1] | arb_grt_from_VC3[1] | arb_grt_from_VC4[1]) & (reqVCfromVC1 == selOutVCtoVC1); 
assign VCgranted[2] = (arb_grt_from_VC0[2] | arb_grt_from_VC1[2] | arb_grt_from_VC2[2] | arb_grt_from_VC3[2] | arb_grt_from_VC4[2]) & (reqVCfromVC2 == selOutVCtoVC2); 
assign VCgranted[3] = (arb_grt_from_VC0[3] | arb_grt_from_VC1[3] | arb_grt_from_VC2[3] | arb_grt_from_VC3[3] | arb_grt_from_VC4[3]) & (reqVCfromVC3 == selOutVCtoVC3); 
assign VCgranted[4] = (arb_grt_from_VC0[4] | arb_grt_from_VC1[4] | arb_grt_from_VC2[4] | arb_grt_from_VC3[4] | arb_grt_from_VC4[4]) & (reqVCfromVC4 == selOutVCtoVC4); 

assign outVCAvailableReset[0] = arb_grt_from_VC0[0] & VCgranted[0] | arb_grt_from_VC0[1] & VCgranted[1] | arb_grt_from_VC0[2] & VCgranted[2] | arb_grt_from_VC0[3] & VCgranted[3] | arb_grt_from_VC0[4] & VCgranted[4];
assign outVCAvailableReset[1] = arb_grt_from_VC1[0] & VCgranted[0] | arb_grt_from_VC1[1] & VCgranted[1] | arb_grt_from_VC1[2] & VCgranted[2] | arb_grt_from_VC1[3] & VCgranted[3] | arb_grt_from_VC1[4] & VCgranted[4];
assign outVCAvailableReset[2] = arb_grt_from_VC2[0] & VCgranted[0] | arb_grt_from_VC2[1] & VCgranted[1] | arb_grt_from_VC2[2] & VCgranted[2] | arb_grt_from_VC2[3] & VCgranted[3] | arb_grt_from_VC2[4] & VCgranted[4];
assign outVCAvailableReset[3] = arb_grt_from_VC3[0] & VCgranted[0] | arb_grt_from_VC3[1] & VCgranted[1] | arb_grt_from_VC3[2] & VCgranted[2] | arb_grt_from_VC3[3] & VCgranted[3] | arb_grt_from_VC3[4] & VCgranted[4];
assign outVCAvailableReset[4] = arb_grt_from_VC4[0] & VCgranted[0] | arb_grt_from_VC4[1] & VCgranted[1] | arb_grt_from_VC4[2] & VCgranted[2] | arb_grt_from_VC4[3] & VCgranted[3] | arb_grt_from_VC4[4] & VCgranted[4];

endmodule