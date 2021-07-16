// delete loading gif and lazy load pictures so that the website loads faster

toad = () => {
  const pic_lazyload = [
    "DSC_5209",
    "DSC_4853",
    "DSC_5066",
    "DSC_4875",
    "DSC_4956",
    "DSC_4967",
    "DSC_5015",
    "newPicture1",
    "newPicture2",
    "newPicture3"
  ];
  pic_lazyload.forEach(function(ele, index) {
    var src = "/static/images/" + ele + ".jpg";
    var item = ".item" + index + "-slick1";
    $(item).css("background-image", "url(" + src + ")");
    var gif = item + " > img";
    $(gif).remove();
  });
};
