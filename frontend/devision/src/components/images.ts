export interface images{
    filename: string;
    index: number;
    url: string;
}

export interface predictions extends images{
    prediction: number;
}
