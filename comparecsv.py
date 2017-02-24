import csv

## ---------------------------------------- Config Section ---------------------------------------- ##

facebook_file = 'input.csv'
salesforce_file = 'sf_fb_posts.csv'
final_file = 'final.csv'

## -------------------------------------- End Config Section -------------------------------------- ##

if __name__ == '__main__':
    f1 = open(facebook_file)
    f1_reader = csv.reader(f1)
    f1_data = list(f1_reader)

    f2 = open(salesforce_file)
    f2_reader = csv.reader(f2)
    f2_data = list(f2_reader)

    cnt = 1
    sf_post_list = []
    for data in f2_data[1:]:
        line = filter(None, data[2].splitlines())
        post = ' '.join(x for x in line)
        sf_post_list.append(post)

    for data in f1_data[1:]:
        cnt += 1
        line = filter(None, data[4].splitlines())
        try:
            line1 = line[4]
            line2 = line[3]
        except IndexError as e:
            try:
                line1 = line[3]
                line2 = line[2]
            except IndexError as e:
                try:
                    line1 = line[2]
                    line2 = line[1]
                except IndexError as e:
                    try:
                        line1 = line[1]
                        line2 = line[0]
                    except IndexError as e:
                        line1 = line[0]
                        line2 = line[0]
        for text in sf_post_list:
            if line2 in text and line1 in text:
                print 'Row no: %s\ntext1 is : %s\ntext2 is: %s\n\n' % (cnt,line1,line2)
                print
                break
        # print '%s : %s'%(cnt,line1)
        # if cnt == 70:
        #     break
