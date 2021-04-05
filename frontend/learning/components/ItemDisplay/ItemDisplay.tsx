import React from 'react';
import PropTypes from 'prop-types';

import CharDisplay from './CharacterDisplay/CharDisplay';
import WordDisplay from './WordDisplay/WordDisplay';
import RadDisplay from './RadicalDisplay/RadDisplay';

import '@learning.styles/ItemDisplay.css';

import { ItemDescriptor } from '@interfaces/CoreItem';
import styled from 'styled-components';

const NextButton = styled.button`
    display: block;
    border: 1px solid var(--main-theme-color);
    color: var(--main-theme-color);
    background-color: white;
    padding: 0.4em 2em;
    margin-bottom: 25px;
    text-align: right;
    transition: all 150ms ease-in-out;
    border-radius: 3px;
    font-size: 0.9em;
  
    &:hover {
        background-color: var(--main-theme-color);
        color: white;
    }
`;

/**
 * Statically display an item (word, character, or radical) 
 * using an ItemDescriptor.
 */
export default function ItemDisplay(props: ItemDescriptor) {
    
    const renderSwitch = (type, qid) => {
        switch (type) {
        case 'character':
            return (<CharDisplay qid={qid} />);
        case 'radical':
            return <RadDisplay qid={qid} />;
        case 'word':
            return <WordDisplay qid={qid} />;
        default:
            return ;
        }
    };

    const renderNext = () => {
        if (props.onActionNext != null)
            return (
                <div>
                    <NextButton onClick={() => props.onActionNext()}>
                        Next
                    </NextButton>
                </div>
            );
    };

    return (
        <>
            <div className='content-card-container box-shadow'
                ref={props.displayRef} tabIndex={0} style={{outline: 'none'}}
            >
                { renderSwitch(props.type, props.qid) }
            </div>
            { renderNext() }
        </>
    );
}

ItemDisplay.propTypes = {
    type: PropTypes.string,
    qid: PropTypes.number,
    onActionNext: PropTypes.func,
    displayRef: PropTypes.any, // not sure which type 
};