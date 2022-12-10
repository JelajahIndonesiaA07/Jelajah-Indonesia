$(document).ready( () =>{
    // diambil dari 
    // https://stackoverflow.com/a/25490531
    const getCookieValue = (name) => (
        document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)')?.pop() || ''
      )
      
    const nama = getCookieValue('nama');
    const umur = getCookieValue('umur');
    const gender = getCookieValue('gender');
    const vaksin = getCookieValue('vaksin');
    const negara = getCookieValue('negara');
    const tujuan = getCookieValue('tujuan');
    const prov = getCookieValue('prov');
    const kontak = getCookieValue('kontak');


    console.log(nama)
    console.log(umur)
    console.log(gender)
    console.log(vaksin)
    console.log(negara)
    console.log(tujuan)
    console.log(prov)
    console.log(kontak)
    
    $("#nama").text(`: ${nama}`);
    $("#umur").text(`: ${umur}`);
    $("#gender").text(`: ${gender}`);
    if (vaksin === "sudah"){
        $("#vaksin").text(": ✅");
    }
    else {
        $("#vaksin").text(": ❌");
    }
    $("#negara").text(`: ${negara}`);
    $("#tujuan").text(`: ${tujuan}`);
    $("#prov").text(`: ${prov}`);
    $("#kontak").text(`: ${kontak}`);
    $('button').text("Dapatkan info lokasi tempat wisata");
    
    $("#con-hasil").slideDown(1000, () =>{
        $("#con-flav").slideDown(1000, () => {
            $("#con-btn").slideDown(1000)
        })
    });
    console.log(nama)
})