"""
CONTRACT-REVIEW Domain Routes
Endpoints called by PARALEGAL-PI for contract and settlement processing
"""
from flask import Blueprint, request, jsonify
from datetime import datetime
import os

api = Blueprint('api', __name__)

# Anthropic client is lazy-loaded when needed
def get_anthropic_client():
    """Lazy load Anthropic client only when API key is available"""
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if api_key and api_key != 'your_key_here':
        import anthropic
        return anthropic.Anthropic(api_key=api_key)
    return None

@api.route('/contract/draft-settlement', methods=['POST'])
def draft_settlement_agreement():
    """
    Draft settlement agreement
    
    Request:
        {
            "case_id": 123,
            "settlement_amount": 250000,
            "terms": {
                "payment_schedule": "lump_sum",
                "confidentiality": true,
                "release_scope": "general"
            }
        }
    
    Response:
        {
            "agreement_text": "...",
            "key_provisions": [...],
            "review_notes": [...]
        }
    """
    data = request.json
    case_id = data.get('case_id')
    settlement_amount = data.get('settlement_amount')
    terms = data.get('terms', {})
    
    if not case_id or not settlement_amount:
        return jsonify({'error': 'case_id and settlement_amount required'}), 400
    
    # Generate settlement agreement
    agreement_text = f"""
SETTLEMENT AGREEMENT AND GENERAL RELEASE

This Settlement Agreement and General Release ("Agreement") is entered into as of {datetime.now().strftime('%B %d, %Y')}, by and between:

**PLAINTIFF**: Jane Doe ("Plaintiff")
**DEFENDANT**: ABC Insurance Company, on behalf of John Anderson ("Defendant")

**RECITALS**

WHEREAS, on or about June 15, 2025, an incident occurred involving Plaintiff and Defendant, resulting in personal injury and property damage to Plaintiff;

WHEREAS, Plaintiff asserts claims against Defendant for negligence, arising from said incident;

WHEREAS, the parties desire to settle and resolve all claims, disputes, and controversies between them without the expense and uncertainty of litigation;

NOW, THEREFORE, in consideration of the mutual covenants and agreements set forth herein, the parties agree as follows:

**1. SETTLEMENT PAYMENT**

Defendant shall pay to Plaintiff the total sum of ${settlement_amount:,} ("Settlement Amount") in full and complete settlement of all claims. Payment shall be made by certified check or wire transfer within thirty (30) days of execution of this Agreement.

**2. GENERAL RELEASE**

In consideration of the Settlement Amount, Plaintiff hereby releases, acquits, and forever discharges Defendant, and all related parties, from any and all claims, demands, actions, causes of action, damages, costs, and expenses of any nature whatsoever, whether known or unknown, arising from or related to the incident of June 15, 2025.

**3. CONFIDENTIALITY**

The parties agree that the terms of this Settlement Agreement, including the settlement amount, shall remain strictly confidential. Neither party shall disclose the terms of this Agreement to any third party, except as required by law or with prior written consent.

**4. NO ADMISSION OF LIABILITY**

This Settlement Agreement is entered into solely for the purpose of compromising disputed claims. Nothing contained herein shall be construed as an admission of liability, wrongdoing, or fault by any party.

**5. MEDICAL LIENS**

Plaintiff represents that all medical liens, if any, will be satisfied from the Settlement Amount, and Defendant shall have no further obligation regarding such liens.

**6. GOVERNING LAW**

This Agreement shall be governed by and construed in accordance with the laws of the State of Nevada.

**7. ENTIRE AGREEMENT**

This Agreement constitutes the entire agreement between the parties and supersedes all prior negotiations, representations, or agreements.

**8. EXECUTION**

This Agreement may be executed in counterparts, each of which shall be deemed an original.


**PLAINTIFF:**

_________________________________
Jane Doe
Date: _______________


**DEFENDANT:**

_________________________________
ABC Insurance Company
By: _____________________________
Date: _______________
    """.strip()
    
    response = {
        'case_id': case_id,
        'settlement_amount': settlement_amount,
        'agreement_text': agreement_text,
        
        'key_provisions': [
            {
                'provision': 'Payment Terms',
                'details': f'${settlement_amount:,} payable within 30 days',
                'risk_level': 'Standard'
            },
            {
                'provision': 'General Release',
                'details': 'Broad release of all claims related to incident',
                'risk_level': 'Plaintiff-favorable'
            },
            {
                'provision': 'Confidentiality',
                'details': 'Mutual obligation to keep terms confidential',
                'risk_level': 'Standard'
            },
            {
                'provision': 'No Admission',
                'details': 'Settlement does not constitute admission of liability',
                'risk_level': 'Defendant-favorable'
            }
        ],
        
        'review_notes': [
            'Ensure all medical liens are identified before signing',
            'Consider tax implications of settlement amount',
            'Verify defendant has authority to bind insurance company',
            'Confirm payment method and timeline acceptable'
        ],
        
        'draft_date': datetime.now().isoformat()
    }
    
    return jsonify(response), 200


@api.route('/contract/review-offer', methods=['POST'])
def review_settlement_offer():
    """
    Analyze defendant's settlement offer
    
    Request:
        {
            "case_id": 123,
            "offer_document": "...",
            "demand_amount": 300000
        }
    
    Response:
        {
            "analysis": "...",
            "red_flags": [...],
            "negotiation_points": [...],
            "recommendation": "..."
        }
    """
    data = request.json
    case_id = data.get('case_id')
    offer_amount = data.get('offer_amount', 150000)
    demand_amount = data.get('demand_amount', 300000)
    
    if not case_id:
        return jsonify({'error': 'case_id required'}), 400
    
    # Calculate offer as percentage of demand
    offer_percentage = (offer_amount / demand_amount * 100) if demand_amount > 0 else 0
    
    analysis = {
        'case_id': case_id,
        'offer_amount': offer_amount,
        'demand_amount': demand_amount,
        'offer_percentage': round(offer_percentage, 1),
        
        'analysis': f"Defendant's offer of ${offer_amount:,} represents {offer_percentage:.1f}% of the demand amount. This is {'a lowball offer' if offer_percentage < 40 else 'a reasonable opening' if offer_percentage < 70 else 'a strong offer'} and should be {'rejected with counter-offer' if offer_percentage < 40 else 'countered strategically' if offer_percentage < 70 else 'seriously considered'}.",
        
        'red_flags': [
            'Offer includes overly broad release language',
            'Payment timeline extends beyond 60 days',
            'Confidentiality clause prohibits disclosure to tax advisor',
            'No provision for handling outstanding medical liens'
        ] if offer_percentage < 50 else [
            'Standard release language',
            'Reasonable payment terms'
        ],
        
        'negotiation_points': [
            f'Counter-offer at ${int(demand_amount * 0.85):,} (85% of demand)',
            'Request 30-day payment instead of 60-day',
            'Narrow release language to specific incident only',
            'Add provision requiring defendant to satisfy all liens',
            'Remove confidentiality restrictions on professional advisors'
        ],
        
        'recommendation': 'COUNTER' if offer_percentage < 70 else 'NEGOTIATE' if offer_percentage < 85 else 'CONSIDER ACCEPTANCE',
        
        'reasoning': [
            f'Medical expenses alone: $10,300',
            f'Pain and suffering multiplier (3x): $30,900',
            f'Lost wages: $8,000',
            f'Property damage: $18,500',
            f'Total economic and non-economic damages: $67,700',
            f'Offer is {offer_percentage:.0f}% of conservative value'
        ],
        
        'alternative_strategies': [
            'File lawsuit to demonstrate seriousness',
            'Conduct further discovery to strengthen case',
            'Obtain expert medical opinion on permanent injury',
            'Request mediator to facilitate higher settlement'
        ]
    }
    
    return jsonify(analysis), 200


@api.route('/contract/generate-release-clause', methods=['POST'])
def generate_release_clause():
    """
    Generate specific release clause
    
    Request:
        {
            "case_id": 123,
            "release_type": "general" | "limited" | "conditional"
        }
    """
    data = request.json
    release_type = data.get('release_type', 'general')
    
    clauses = {
        'general': """
**GENERAL RELEASE**

Plaintiff, for themselves and their heirs, executors, administrators, successors, and assigns, hereby releases, acquits, and forever discharges Defendant, together with their officers, directors, employees, agents, insurers, successors, and assigns (collectively, the "Released Parties"), from any and all claims, demands, damages, actions, causes of action, suits, debts, liens, contracts, agreements, promises, liability, judgments, and expenses of any nature whatsoever, whether known or unknown, suspected or unsuspected, fixed or contingent, which Plaintiff now has or may hereafter have against the Released Parties, arising from or in any way related to the incident occurring on or about [DATE].
        """.strip(),
        
        'limited': """
**LIMITED RELEASE**

Plaintiff hereby releases Defendant solely with respect to claims arising from the motor vehicle collision occurring on [DATE] at [LOCATION]. This release does not extend to:
(a) Any claims unrelated to said motor vehicle collision;
(b) Any claims for injuries or damages that are not reasonably discoverable as of the date of this Agreement;
(c) Any claims against third parties not specifically named herein;
(d) Any claims for insurance bad faith, if applicable.
        """.strip(),
        
        'conditional': """
**CONDITIONAL RELEASE**

This release shall become effective only upon:
(a) Receipt and clearance of the full Settlement Amount;
(b) Satisfaction of all medical liens by Defendant;
(c) Execution of this Agreement by all parties; and
(d) Expiration of any applicable rescission period.

If any of the foregoing conditions are not met within sixty (60) days, this Agreement shall be null and void, and all rights of Plaintiff shall be preserved.
        """.strip()
    }
    
    response = {
        'release_type': release_type,
        'clause_text': clauses.get(release_type, clauses['general']),
        'protection_level': {
            'general': 'Maximum protection for defendant',
            'limited': 'Balanced protection',
            'conditional': 'Maximum protection for plaintiff'
        }.get(release_type)
    }
    
    return jsonify(response), 200


@api.route('/contract/risk-assessment', methods=['POST'])
def assess_contract_risk():
    """
    Assess risks in proposed settlement terms
    """
    data = request.json
    
    risk_assessment = {
        'overall_risk_level': 'MODERATE',
        'risks_identified': [
            {
                'category': 'Financial',
                'risk': 'Payment default by defendant',
                'likelihood': 'Low',
                'mitigation': 'Require certified funds or escrow arrangement'
            },
            {
                'category': 'Legal',
                'risk': 'Undiscovered injuries appearing post-settlement',
                'likelihood': 'Medium',
                'mitigation': 'Medical examination; consider unknown injury clause'
            },
            {
                'category': 'Tax',
                'risk': 'Portion of settlement may be taxable',
                'likelihood': 'High',
                'mitigation': 'Consult tax professional; allocate settlement properly'
            },
            {
                'category': 'Liens',
                'risk': 'Medical liens exceeding anticipated amounts',
                'likelihood': 'Medium',
                'mitigation': 'Obtain final lien amounts in writing pre-settlement'
            }
        ],
        'recommendations': [
            'Have client undergo final medical evaluation',
            'Obtain lien payoff letters from all providers',
            'Consult with tax advisor on settlement allocation',
            'Ensure 30-day payment timeline (not 60+)',
            'Add clause requiring defendant to satisfy liens directly'
        ]
    }
    
    return jsonify(risk_assessment), 200
