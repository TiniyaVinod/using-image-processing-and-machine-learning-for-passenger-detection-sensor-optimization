function [human_image, num_human] = humanDetection(image, classifier_model, human_size, output_img_size)
% #codegen
% This function finds a face in image and return only cropped face image
% with size output_img_size
%
% parameters :
%               image : [width, height]              ; 3 channel image
%               classifier_model : classifier model string
%               human_size : [width, height]   ; minimum human image size
%               output_img_size : [width, height] ; expected output image
%                                                   size of this function
% return value : 
%               human_image : cropped image with face    ; if found a face
%                          : image                      ; if not found a
%                                                         human in image or
%                                                         more than a human
%                                                         is found
%               num_human   : 0 ;    default value and return this when found
%                                   no human at all          
% cautions : this function will return face_image iff there is only 1 face
% in the image, otherwise it will return [] 


% Init output
human_image = image;
num_human = 0;

if size(image,3) ~= 3
    disp('An input image must be 3 channel');
    return
end

human_detector = vision.CascadeObjectDetector('ClassificationModel', classifier_model, 'MinSize', human_size );
human_location = human_detector(image);

% not found human
if isempty(human_location)
    return;
end

human_image = size(human_location,1);

% found multiple humans
if human_image > 1
    return;
end

% found a human
human_image = image( human_location(2):human_location(2)+human_location(4), human_location(1):human_location(1)+human_location(3), : );

human_image = imresize(human_image, output_img_size);

end