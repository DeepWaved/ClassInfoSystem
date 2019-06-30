import axios from 'axios';

let base = ' http://127.0.0.1:5000/api';  //服务器地址


export const requestLogin = async params => {
    const res = await axios({
        method: 'POST',
        url: `${base}/login`,
        auth: params
    });
    return res.data;
};

export const setpwd = async params => {
    const res = await axios.post(`${base}/setpwd`, params);
    return res.data;
};

export const requestSignUp = async params => {
    const res = await axios.post(`${base}/signup`, params);
    return res.data;
}

export const requestCost = async params => {
    const res = await axios.post(`${base}/requestcost`, params);
    return res.data;
}

export const requestMeeting = async params => {
    const res = await axios.post(`${base}/requestmeeting`, params);
    return res.data;
}

export const requestNewNotice = async params => {
    const res = await axios.post(`${base}/requestNewNotice`, params);
    return res.data;
}

export const requestNewHomework = async params => {
    const res = await axios.post(`${base}/requestNewHomework`, params);
    return res.data;
}

export const requestNewQuestion = async params => {
    const res = await axios.post(`${base}/requestNewQuestion`, params);
    return res.data;
}

export const fileUpload = async params => {
    const res = await axios.post(`${base}/fileUpload`, params, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
    return res.data;
}

export const removeUser = params => {
    return axios.get(`${base}/user/remove`, { params: params });
};

export const removeNotice = params => {
    return axios.get(`${base}/notice/remove`, { params: params });
};

export const getAdminMessage = async params => {
    const res = await axios.get(`${base}/getadmin`, params);
    return res.data;
}

export const getMeeting = async params => {
    const res = await axios.get(`${base}/getmeeting`, params);
    return res.data;
}

export const getCost = async params => {
    const res = await axios.get(`${base}/getcost`, params);
    return res.data;
}

export const getUser = async params => {
    const res = await axios.get(`${base}/getuser`, params);
    return res.data;
}

export const getNotice = async params => {
    const res = await axios.get(`${base}/notice/get`, params);
    return res.data;
}

export const getExcel = async params => {
    const res = await axios.post(`${base}/homework/excel`, params);
    return res.data;
}

export const getZip = async params => {
    const res = await axios.post(`${base}/homework/zip`, params);
    return res.data;
}

export const getHomework = async params => {
    const res = await axios.get(`${base}/homework/get`, { params: params });
    return res.data;
}

export const getAllHomework = async params => {
    const res = await axios.get(`${base}/homework/getall`, { params: params });
    return res.data;
}

export const getHomeworkRecord = async params => {
    const res = await axios.get(`${base}/homeworkRecord/get`, { params: params });
    return res.data;
}

export const getUserInfo = async params => {
    const res = await axios.get(`${base}/getUserInfo`, { params: params });
    return res.data;
}