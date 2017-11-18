var server_url = 'http://localhost:5000'

var $inputForm = $('#input-form').show();
var $popup = $('#popup').hide();
var $popupText = $('#popup-text').hide();
var $popupSpinner = $('#popup-spinner').hide();
var $popupButton = $('#popup-button').hide();
var $mainPage = $('#main-page').hide();
var $qrDisplay = $('#qr-display').hide();
var $informationField = $('#information-field').hide();
var $nameDiv = $('#name-div').hide();
var $balanceDiv = $('#balance-div').hide();
var $transactionSpinner = $('#transaction-history-spinner').hide();
var $transactionTable = $('#transaction-history-table').hide();

$('#input-form').find('input, textarea').on('keyup blur focus', function (e) {
  
  var $this = $(this),
      label = $this.prev('label');

	  if (e.type === 'keyup') {
			if ($this.val() === '') {
          label.removeClass('active highlight');
        } else {
          label.addClass('active highlight');
        }
    } else if (e.type === 'blur') {
    	if( $this.val() === '' ) {
    		label.removeClass('active highlight'); 
			} else {
		    label.removeClass('highlight');   
			}   
    } else if (e.type === 'focus') {
      
      if( $this.val() === '' ) {
    		label.removeClass('highlight'); 
			} 
      else if( $this.val() !== '' ) {
		    label.addClass('highlight');
			}
    }

});

$('.tab a').on('click', function (e) {
  
  e.preventDefault();
  
  $(this).parent().addClass('active');
  $(this).parent().siblings().removeClass('active');
  
  target = $(this).attr('href');

  $('.tab-content > div').not(target).hide();
  
  $(target).fadeIn(600);
  
});

$('#register-button').on('click', function(e) {
  var firstName =  $('#first-name-input').val();
  var lastName =  $('#last-name-input').val();
  var emailInput = $('#email-input').val();
  var passwordInput = $('#password-input').val();
  $inputForm.hide();
  $popup.show();
  $popupText.text('Signing Up').show();
  $popupSpinner.show();
  $popupButton.hide();
  $.ajax({
    type: 'POST',
    url: server_url + "/api/account/register",
    data: {
      name: firstName + ' ' + lastName,
      email: emailInput,
      password: passwordInput
    },
    success: function(data) {
      $inputForm.hide();
      $popup.hide();
      $mainPage.show();


    },
    error: function(data) {
      $popupText.text('Error Occured in Registration')
      $popupButton.html('Back to Sign Up').show();
      $popupSpinner.hide();
    }
  });
});

$('#login-button').on('click', function(e) {
  var email = $('#email-field').val();
  var password = $('#password-field').val();
  $inputForm.hide();
  $popup.show();
  $popupText.text('Logging In').show();
  $popupSpinner.show();
  $popupButton.hide();

  $.ajax({
    type: 'POST',
    url: server_url + '/api/account/user',
    data: {
      email: email,
      password: password
    },
    success: function(data) {
      $inputForm.hide();
      $popup.hide();
      $mainPage.show();

      $qrDisplay.show();
      $nameDiv.html('Name: William Li').show();
      $balanceDiv.html('Balance: $500').show();
      $transactionSpinner.show();
    },
    error: function(data) {
      // $popupText.text('Could not find account')
      // $popupButton.html('Back to Login').show();
      // $popupSpinner.hide();
      $inputForm.hide();
      $popup.hide();
      $mainPage.show();

      $qrDisplay.qrcode({
        width: 512,
        height: 512,
        text: "loooooolol"
      }).show();
      $informationField.show();
      $nameDiv.html('Name: William Li').show();
      $balanceDiv.html('Balance: $500').show();
      $transactionSpinner.show();
    }
  });
});

$popupButton.on('click', function(e) {
  $popup.hide();
  $popupText.hide();
  $popupSpinner.hide();
  $popupButton.hide();
  $inputForm.show();
})
