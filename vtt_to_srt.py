#encoding=utf-8

# -------------------------------------------------------------------- #
# A tool for changing vtt files to srt files
# our tool supports different styles of vtt files
# -------------------------------------------------------------------- #
#   Style 1:
#       WEBVTT
#
#       00:00:00.220 --> 00:00:01.692
#       Okay, good morning everyone.
#
#       00:00:01.692 --> 00:00:05.740
#       We're gonna get started with our
#       first tutorial in this room.
# -------------------------------------------------------------------- #
#   Style 2:
#       WEBVTT
#       Kind: captions
#       Language: en
#       Style:
#       ::cue(c.colorCCCCCC) { color: rgb(204,204,204);
#        }
#       ::cue(c.colorE5E5E5) { color: rgb(229,229,229);
#        }
#
#       00:00:00.000 --> 00:00:06.089 align:start position:19%
#       <c.colorE5E5E5>welcome<00:00:00.989><c> everyone</c><00:00:01.230><c> to</c><00:00:01.589><c> the</c><00:00:02.250><c> first</c><00:00:02.460><c> lecture</c><00:00:02.939><c> of</c></c>
#
#       00:00:03.389 --> 00:00:09.240 align:start position:19%
#       our<00:00:03.780><c> new</c><00:00:04.380><c> course</c><c.colorE5E5E5><00:00:04.740><c> deep</c><00:00:05.430><c> learning</c><00:00:05.549><c> for</c><00:00:05.819><c> natural</c></c>
#
#       00:00:06.089 --> 00:00:11.519 align:start position:19%
#       language<00:00:06.299><c> processing</c><00:00:06.330><c> time</c><00:00:08.429><c> for</c><c.colorCCCCCC><00:00:08.580><c> quantum</c><00:00:08.970><c> i'm</c></c>
# -------------------------------------------------------------------- #
# Time:     2017-03-17
# Autuor:   JunjieLi@CASIA
# -------------------------------------------------------------------- #

import usefulAPI

def get_init_subtitles_dict():
    subtitle_dict = {}
    subtitle_dict['number'] = 0
    subtitle_dict['time'] = ''
    subtitle_dict['content'] = ''
    return subtitle_dict

def print_out_subtitle_con_list(subtitle_con_list,out_file):
    out_con_list = []
    for subtitle_dict in subtitle_con_list:
        out_con_list.append(str(subtitle_dict['number']))
        out_con_list.append(subtitle_dict['time'])
        out_con_list.append(subtitle_dict['content'])
        out_con_list.append('')
    open(out_file,'w+').write('\n'.join(out_con_list))

def get_content_str_info(vtt_str_con):
    vtt_str_con_list = vtt_str_con.strip().split('<c>')
    srt_str_con_list = []
    for i in range(0,len(vtt_str_con_list)):
        temp_str = vtt_str_con_list[i]
        temp_add_space_str = temp_str.replace('>','> ')
        t_str = temp_add_space_str[temp_add_space_str.find(' '):len(temp_add_space_str)]
        ans_str = t_str[t_str.find(' '):t_str.find('<')]
        if i == 0: ans_str = ans_str.replace(' ','')
        srt_str_con_list.append(ans_str)
    return ''.join(srt_str_con_list)

def change_vtt_style_1_to_srt(vtt_file,srt_file):
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

def change_vtt_style_2_to_srt(vtt_file,srt_file):
    subtitle_con_list = []
    line_con_list = open(vtt_file,'r').readlines()
    line_num = 1
    is_begin_record = False
    for line_con in line_con_list:
        line_con = line_con.strip()
        if line_con.find(' --> ') != -1:
            is_begin_record = True
        if is_begin_record:
            if line_con.find(' --> ') != -1:
                subtitle_dict = get_init_subtitles_dict()
                is_begin_record = True
                temp_line_con = line_con.replace('.',',')
                temp_list = temp_line_con.split(' ')
                if len(temp_list) <= 3: continue
                subtitle_time_info = temp_list[0] + ' ' + temp_list[1] + ' ' + temp_list[2]
                subtitle_dict['number'] = line_num
                subtitle_dict['time'] = subtitle_time_info
                line_num = line_num + 1
            elif line_con != '':
                srt_str_con = get_content_str_info(line_con)
                subtitle_dict['content'] = srt_str_con.strip()
                subtitle_con_list.append(subtitle_dict)

    new_subtitle_con_list = []
    for i in range(0,len(subtitle_con_list)-1):
        if i % 2 == 1: continue
        else:
            subtitle_dict = get_init_subtitles_dict()
            subtitle_dict['number'] = (subtitle_con_list[i]['number'] + 1) / 2
            subtitle_dict['time'] = subtitle_con_list[i]['time']
            subtitle_dict['content'] = subtitle_con_list[i]['content'] + ' ' + subtitle_con_list[i+1]['content']
            new_subtitle_con_list.append(subtitle_dict)


    print_out_subtitle_con_list(new_subtitle_con_list,srt_file)



def deal_with_a_filefold(in_file_fold,vtt_file_style = '2'):
    vtt_file_list = usefulAPI.get_dir_files(in_file_fold,is_contain_dir=True)
    srt_file_list = [vtt_file.replace('.vtt','.srt') for vtt_file in vtt_file_list]
    for vtt_file,srt_file in zip(vtt_file_list,srt_file_list):
         if vtt_file_style == '2':
            change_vtt_style_2_to_srt(vtt_file,srt_file)
         else:
            change_vtt_style_1_to_srt(vtt_file,srt_file)

if __name__ == '__main__':

    vtt_file = './vtt_style_1_files/Variational-Inference-Foundations-and-Modern-Methods_en.vtt'
    srt_file = './srt_files/Variational-Inference-Foundations-and-Modern-Methods_en.srt'
    change_vtt_style_1_to_srt(vtt_file,srt_file)

    vtt_file = './vtt_style_2_files/Deep Learning for NLP at Oxford 2017 - Leacure 1a - Introduction [Phil Blunsom]-RP3tZFcC2e8.en.vtt'
    srt_file = './srt_files/Deep Learning for NLP at Oxford 2017 - Leacure 1a - Introduction [Phil Blunsom]-RP3tZFcC2e8.en.srt'
    change_vtt_style_2_to_srt(vtt_file,srt_file)

    deal_with_a_filefold(in_file_fold = './vtt_style_2_files/')





