console.log('masuk')
$(document).ready( () =>{

    $("#q").slideDown(1000, () => {
        $("#nama").slideDown(1000, () => {
            $("#next-q").slideDown(1000);
        });
    });
    

    let listPertanyaan = [
        "Berapakah umur anda?", 
        "Apakah jenis kelamin anda?",
        "Apakah anda sudah menerima vaksin Covid-19?",
        "Darimana negara asalmu?",
        "Apakah tujuan anda berkunjung ke Indonesia?", 
        "Apakah provinsi tujuan anda?",
        "Nomor telepon yang dapat dihubungi",
        "Kesan/Pesan selama di Indonesia",
    ];
    
    // let radio = [3, 4, 6];
    
    let pertanyaanCounter = 0;
    let nama = "-";
    let umur = "-";
    let gender = "-";
    let vaksin = "-";
    let negara = "-";
    let tujuan = "-";
    let provinsi = "-";
    let kontak = "-";
    
    $("#next-q").click(function(){
        console.log(pertanyaanCounter);
        if(pertanyaanCounter === 0){
            if ($("#nama").val().length === 0) {
                alert("Harap isi nama anda");
                return
            }       
            $("#q").fadeOut(300);     
            $("#a0-con").fadeOut(300, () => {
                $("#question-navigator").fadeOut(300, () =>{
                    $("#next-q").text("Selanjutnya");
                })
            });
            
        }
        
        pertanyaanCounter++;
        if(pertanyaanCounter === 9){
            cekSemua();
            return
        }
    
        // if(radio.includes(pertanyaanCounter)){
        //     if(!$(`input[name='a${pertanyaanCounter}']:checked`).val()){
        //         alert("Pertanyaan ini wajib dijawab");
        //         pertanyaanCounter--;
        //         return;
        //     }
        // }
    
        $("#question-navigator").fadeOut(300, () =>{
            if(pertanyaanCounter > 1) $("#back-q").show();
            // hide yg sebelumnya
            if(pertanyaanCounter === 1){
                $("#q").fadeOut(300, () => {
                    $("#question").text(listPertanyaan[0]);
                    $("#q").fadeIn(300);
                    $("#a" + pertanyaanCounter + "-con").fadeIn(300);
                    $("#question-navigator").fadeIn(300);
                });
                return;
            }
            $("#q").fadeOut(300);
            $("#a" + (pertanyaanCounter - 1) + "-con").fadeOut(300, () => {
                $("#question").text(listPertanyaan[pertanyaanCounter-1]);
                $("#q").fadeIn(300);
                $("#a" + pertanyaanCounter + "-con").fadeIn(300);
                $("#question-navigator").fadeIn(300);   
            });
            
        })
    })
    
    $("#back-q").click(function(){
        pertanyaanCounter--;
        
    
        $("#question-navigator").fadeOut(300, () =>{
            if(pertanyaanCounter <= 1) $("#back-q").hide();
            // hide yg setelahnya
            $("#q").fadeOut(300);
            $("#a" + (pertanyaanCounter + 1) + "-con").fadeOut(300, () => {
                $("#question").text(listPertanyaan[pertanyaanCounter-1]);
                $("#q").fadeIn(300);
                $("#a" + pertanyaanCounter + "-con").fadeIn(300);
                $("#question-navigator").fadeIn(300);
            })
        })
    });
    
    function cekSemua(){
        pertanyaanCounter--;
        nama = $('#nama').val();
        console.log(nama);
        umur = $("input[type='number'][id='umur']").val();
        console.log(umur);
    
        gender = $("input[type='radio'][name='gender']:checked").val();
        console.log(gender);
        vaksin = $("input[type='radio'][name='vaksin']:checked").val();
        console.log(vaksin);
        negara = $('select[name=country-selector] option').filter(':selected').val();
        console.log(negara);
        tujuan = $("input[type='radio'][name='tujuan']:checked").val();
        console.log(tujuan);
        provinsi = $('select[name=provinsi-selector] option').filter(':selected').val();
        console.log(provinsi);
        kontak = $('#kontak').val();
        console.log(kontak);

        document.cookie = `nama=${nama}`
        document.cookie = `umur=${umur}`
        document.cookie = `gender=${gender}`
        document.cookie = `vaksin=${vaksin}`
        document.cookie = `negara=${negara}`
        document.cookie = `tujuan=${tujuan}`
        document.cookie = `prov=${provinsi}`
        document.cookie = `kontak=${kontak}`

        kirim(nama, umur, gender, vaksin, negara, tujuan, provinsi, kontak);
        window.location.replace("./hasil");
    }

    function kirim(nama, umur, gender, vaksin, negara, tujuan, prov, kontak){
        console.log($('form'));
        const csrf = document.getElementsByName("csrfmiddlewaretoken");
        const fd = new FormData();
        fd.append('csrfmiddlewaretoken', csrf[0].value);
        fd.append('nama', nama);
        fd.append('umur', umur);
        fd.append('gender', gender);
        fd.append('vaksin', vaksin);
        fd.append('negara', negara);
        fd.append('tujuan', tujuan);
        fd.append('prov', prov);
        fd.append('kontak', kontak);

        console.log(fd)

        $.ajax({
            url : '',
            type: 'POST',
            enctype: 'multipart/form-data',
            data: fd,
            success: function(response){
                console.log(response);
            },
            error: function(error){
                console.log(error);
            },
            cache: false,
            contentType: false,
            processData: false,
        }) 
    }
})