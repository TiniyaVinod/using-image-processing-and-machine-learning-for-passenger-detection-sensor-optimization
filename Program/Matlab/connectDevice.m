function [cam, connect_status] = connectDevice()
% #codegen
% This function finds and connect camera
% return value :
%               cam : camera object   ; if found device
%                     []              ; if not found device
%               connect_status : true     ; if found device and connected
%                                false    ; if not found device

cam = [];
device_list = webcamlist();

if isempty(device_list)
    disp('No device found');
    connect_status = false;
    return
end
device = device_list{1};

cam = webcam(device);
connect_status = true;
return

end
