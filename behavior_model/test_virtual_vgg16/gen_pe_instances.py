'''
Generate PE instances in "system.sv"
'''

for i in range(7):
    for j in range(8):
        print('''
virtual_pe #(
    .isCaster                    (isCaster_'''+str(i)+'''_'''+str(j)+'''),
    .stream_id                   (stream_id_'''+str(i)+'''_'''+str(j)+''')
)pe_'''+str(i)+'''_'''+str(j)+'''(
    .clk                         (clk),
    .rstn                        (rstn),
    .valid_i_cast                (cast_valid_o['''+str(i)+''']['''+str(j)+''']),
    .data_i_cast                 (cast_data_o['''+str(i)+''']['''+str(j)+''']),
    .ready_o_cast                (pe_cast_ready_o['''+str(i)+''']['''+str(j)+''']),
    .valid_o_cast                (pe_cast_valid_o['''+str(i)+''']['''+str(j)+''']),
    .data_o_cast                 (pe_cast_data_o['''+str(i)+''']['''+str(j)+''']),
    .ready_i_cast                (cast_ready_o['''+str(i)+''']['''+str(j)+''']),
    .valid_i_merge               (merge_valid_o['''+str(i)+''']['''+str(j)+''']),
    .data_i_merge                (merge_data_o['''+str(i)+''']['''+str(j)+''']),
    .ready_o_merge               (pe_merge_ready_o['''+str(i)+''']['''+str(j)+''']),
    .valid_o_merge               (pe_merge_valid_o['''+str(i)+''']['''+str(j)+''']),
    .data_o_merge                (pe_merge_data_o['''+str(i)+''']['''+str(j)+''']),
    .ready_i_merge               (merge_ready_o['''+str(i)+''']['''+str(j)+''']),
    .credit_upd                  (credit_upd['''+str(i)+''']['''+str(j)+'''])
); 
''')