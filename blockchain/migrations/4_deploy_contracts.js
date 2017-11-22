var ConvertLib = artifacts.require("./ConvertLib.sol");
var ProofOfExistence = artifacts.require("./ProofOfExistence.sol");
var HTH = artifacts.require("./HTH.sol");

module.exports = function(deployer) {
  deployer.deploy(ConvertLib);
  deployer.link(ConvertLib, HTH);
  
  deployer.deploy(HTH);
  deployer.deploy(ProofOfExistence);
};
