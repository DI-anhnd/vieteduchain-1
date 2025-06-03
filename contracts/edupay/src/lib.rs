//! CosmWasm Escrow Contract for EduPay Tuition Settlement
//! - eVND (ICS-20) escrow between payer and school
//! - Release on ProofOfEnrollment

use cosmwasm_std::{entry_point, to_binary, Addr, BankMsg, Binary, Coin, Deps, DepsMut, Env, MessageInfo, Response, StdError, StdResult, Uint128};
use cw2::set_contract_version;
use schemars::JsonSchema;
use serde::{Deserialize, Serialize};

const CONTRACT_NAME: &str = "crates.io:edupay-escrow";
const CONTRACT_VERSION: &str = env!("CARGO_PKG_VERSION");

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq, JsonSchema)]
pub struct InstantiateMsg {}

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq, JsonSchema)]
pub struct Escrow {
    pub payer: Addr,
    pub school: Addr,
    pub amount: Coin,
    pub released: bool,
}

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq, JsonSchema)]
pub enum ExecuteMsg {
    Deposit { school: String },
    Release { proof: String },
    Refund {},
}

#[derive(Serialize, Deserialize, Clone, Debug, PartialEq, JsonSchema)]
pub enum QueryMsg {
    GetEscrow { payer: String },
}

pub const ESCROWS: cw_storage_plus::Map<&Addr, Escrow> = cw_storage_plus::Map::new("escrow");

#[entry_point]
pub fn instantiate(
    deps: DepsMut,
    _env: Env,
    _info: MessageInfo,
    _msg: InstantiateMsg,
) -> StdResult<Response> {
    set_contract_version(deps.storage, CONTRACT_NAME, CONTRACT_VERSION)?;
    Ok(Response::default())
}

#[entry_point]
pub fn execute(
    deps: DepsMut,
    _env: Env,
    info: MessageInfo,
    msg: ExecuteMsg,
) -> StdResult<Response> {
    match msg {
        ExecuteMsg::Deposit { school } => try_deposit(deps, info, school),
        ExecuteMsg::Release { proof } => try_release(deps, info, proof),
        ExecuteMsg::Refund {} => try_refund(deps, info),
    }
}

fn try_deposit(deps: DepsMut, info: MessageInfo, school: String) -> StdResult<Response> {
    let amount = info.funds.iter().find(|c| c.denom == "evnd").cloned().ok_or_else(|| StdError::generic_err("No eVND sent"))?;
    let school_addr = deps.api.addr_validate(&school)?;
    let escrow = Escrow {
        payer: info.sender.clone(),
        school: school_addr,
        amount,
        released: false,
    };
    ESCROWS.save(deps.storage, &info.sender, &escrow)?;
    Ok(Response::new().add_attribute("action", "deposit"))
}

fn try_release(deps: DepsMut, info: MessageInfo, proof: String) -> StdResult<Response> {
    let mut escrow = ESCROWS.load(deps.storage, &info.sender)?;
    if escrow.released {
        return Err(StdError::generic_err("Already released"));
    }
    // TODO: verify proof (integration with EduID/EduCert)
    if proof != "valid" {
        return Err(StdError::generic_err("Invalid proof"));
    }
    escrow.released = true;
    ESCROWS.save(deps.storage, &info.sender, &escrow)?;
    let send = BankMsg::Send {
        to_address: escrow.school.to_string(),
        amount: vec![escrow.amount.clone()],
    };
    Ok(Response::new().add_message(send).add_attribute("action", "release"))
}

fn try_refund(deps: DepsMut, info: MessageInfo) -> StdResult<Response> {
    let escrow = ESCROWS.load(deps.storage, &info.sender)?;
    if escrow.released {
        return Err(StdError::generic_err("Already released"));
    }
    let send = BankMsg::Send {
        to_address: escrow.payer.to_string(),
        amount: vec![escrow.amount.clone()],
    };
    ESCROWS.remove(deps.storage, &info.sender);
    Ok(Response::new().add_message(send).add_attribute("action", "refund"))
}

#[entry_point]
pub fn query(deps: Deps, _env: Env, msg: QueryMsg) -> StdResult<Binary> {
    match msg {
        QueryMsg::GetEscrow { payer } => {
            let addr = deps.api.addr_validate(&payer)?;
            let escrow = ESCROWS.may_load(deps.storage, &addr)?;
            to_binary(&escrow)
        }
    }
}
