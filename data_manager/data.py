import csv


def read_csv(filename):
    with open(filename, newline='') as file:
        reader = csv.reader(file)
        data = list(reader)
    return data

def sort_matrix_by_column_with_headers(data,column):
    size = len(data)
    output = []
    output.append(data[0])
    while data != []:
        sorted = [0,0,0,0,0,0,0]
        most = 0 
        for i in range(1,len(data)):
            if int(data[i][column]) > int(sorted[column]):
                sorted = data[i]
                most = i
        if len(output) == size:
            break
        output.append(sorted)
        data.remove(data[most])
    return output

data = [['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image'], ['1', '1493368154', '29', '7', 'How to make lists in Python?', 'I am totally new to this, any hints?', ''], ['2', '1493068124', '15', '9', 'Wordpress loading multiple jQuery Versions', "I developed a plugin that uses the jquery booklet plugin (http://builtbywill.com/booklet/#/) this plugin binds a function to $ so I cann call $('.myBook').booklet();\r\n\r\nI could easy managing the loading order with wp_enqueue_script so first I load jquery then I load booklet so everything is fine.\r\n\r\nBUT in my theme i also using jquery via webpack so the loading order is now following:\r\n\r\njquery\r\nbooklet\r\napp.js (bundled file with webpack, including jquery)", 'images/image1.png'], ['3', '1493015432', '1364', '57', 'Drawing canvas with an image picked with Cordova Camera Plugin', "I'm getting an image from device and drawing a canvas with filters using Pixi JS. It works all well using computer to get an image. But when I'm on IOS, it throws errors such as cross origin issue, or that I'm trying to use an unknown format.\r\n\r\nThis is the code I'm using to draw the image (that works on web/desktop but not cordova built ios app)", '']]
sort_matrix_by_column_with_headers(data, column=2)