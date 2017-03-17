#encoding=utf-8


def change_vtt_to_srt(vtt_file,srt_file):
    line_con_list = open(vtt_file,'r').readlines()
    out_con_list = []
    line_num = 1
    for line_con in line_con_list:
        line_con = line_con.strip()
        if line_con == 'WEBVTT': continue
        if line_con.find(' --> ') != -1:
            out_con_list.append(line_con.replace('.',','))
        elif line_con == '':
            if line_num > 1:
                out_con_list.append(line_con)
            out_con_list.append(str(line_num))
            line_num = line_num + 1
        else:
            out_con_list.append(line_con)
    open(srt_file,'w+').write('\n'.join(out_con_list))


if __name__ == '__main__':
    vtt_file = 'Variational-Inference-Foundations-and-Modern-Methods_en.vtt'
    srt_file = 'Variational-Inference-Foundations-and-Modern-Methods_en.srt'
    change_vtt_to_srt(vtt_file,srt_file)


