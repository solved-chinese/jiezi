
import HanziWriter from 'hanzi-writer';
import React, {} from 'react';
import styled from 'styled-components';
import '@learning.styles/ItemDisplay.css';
import PropTypes from 'prop-types';
import {makeid} from '@utils/utils';

const WordContainer = styled.div`
    display: flex;
    flex-direction: row;
`;

const CharSVGContainer = styled.div`
    font-size: 3.75em;
    font-weight: 200;
    text-align: center;
    color: var(--primary-text);
`;

// Enumeration for states
const WriterState = {
    STANDBY: 'standby',
    PLAYING: 'playing',
    PAUSED: 'paused'
};

/**
 * Render characters with HanziWriter, allowing clicking for
 * stroke order animations.
 */
export default class StrokeGif extends React.Component {

    static propTypes = {
        item: PropTypes.string.isRequired
    };

    constructor(props) {
        super(props);
    }

    componentDidMount() {
        this.writers = this.getWriters(this.itemsTargetIDs, this.items);
        this.writerStates = this.getInitialWriterStates(this.items.length);
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        this.writers = this.getWriters(this.itemsTargetIDs, this.items);
        this.writerStates = this.getInitialWriterStates(this.items.length);
    }

    getWriters(targetIDs, items) {
        return targetIDs.map((value, index) =>
            HanziWriter.create(value, items[index], {
                width: 60,
                height: 65,
                padding: 2,
                strokeAnimationSpeed: 1, // times the normal speed
                delayBetweenStrokes: 5, // ms between strokes
                showOutline: true,
                showCharacter: true,
                strokeColor: '#303545',
                onLoadCharDataError: () => {
                    this.itemsTargetRef[index].current.innerText = items[index];
                }
            })
        );
    }

    getInitialWriterStates(n) {
        let arr = [];
        for (let i = 0; i < n; i++) {
            arr.push(WriterState.STANDBY);
        }
        return arr;
    }

    renderWriterTarget() {
        return this.itemsTargetIDs.map(
            (id, index) =>
                <CharSVGContainer
                    id={id} key={this.itemsTargetIDs[index]} style={{cursor: 'grab'}}
                    onClick={() => this.writerCallback(index)}
                    className='use-chinese'
                    ref={this.itemsTargetRef[index]}
                />
        );
    }

    nextWriterStates(prevStates, index, newState) {
        let arr = prevStates.writerStates.map((v) => v);
        arr[index] = newState;
        return arr;
    }

    writerCallback(index) {
        let writer = this.writers[index];
        switch (this.writerStates[index]) {
        case WriterState.STANDBY:
            writer.animateCharacter({
                onComplete: () => {
                    this.writerStates[index] = WriterState.STANDBY;
                }
            });
            this.writerStates[index] = WriterState.PLAYING;
            break;
        case WriterState.PLAYING:
            writer.pauseAnimation();
            this.writerStates[index] = WriterState.PAUSED;
            break;
        case WriterState.PAUSED:
            writer.resumeAnimation();
            this.writerStates[index] = WriterState.PLAYING;
            break;
        }
    }

    render() {
        this.items = this.props.item.split('');
        this.itemsTargetIDs = this.items.map((value, index) =>
            `writer-target-${index}-${makeid(5)}`);
        this.itemsTargetRef = this.itemsTargetIDs.map(() => React.createRef() );

        return (
            <WordContainer>
                { this.renderWriterTarget() }
            </WordContainer>
        );
    }
}