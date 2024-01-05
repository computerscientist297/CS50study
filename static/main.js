document.addEventListener('DOMContentLoaded', function() {

    let p_colors = document.querySelectorAll('.calendar_p');
    let m_colors = document.querySelectorAll('.calendar_m');

    let p_transparency = [];
    let m_transparency = [];


    for (let i = 0; i < p_colors.length; i++)
    {
        for (let j = 0; j < p_colors.length; j++)
        {
            p_transparency[j] = Number(p_colors[j].innerHTML) / 10;
        }
        p_colors[i].style="background-color: rgba(0, 255, 0," + p_transparency[i] + ")";
    }

    for (let p = 0; p < m_colors.length; p++)
    {
        for (let q = 0; q < m_colors.length; q++)
        {
            m_transparency[q] = Number(m_colors[q].innerHTML) / 10;
        }
        m_colors[p].style="background-color: rgba(0, 0, 255," + m_transparency[p] + ")";

    }
}
);


